import logging
from datetime import datetime
import argparse
from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError
from bson import ObjectId
import os

DATABASE_NAME = "fdr-re"
COLLECTION_NAME = "events"

# Initializing parameters passed as parameters
parser = argparse.ArgumentParser()
parser.add_argument('--connstr', type=str, help='MongoDB connection string', required=True)
parser.add_argument('--startdate', type=str, help='Date from which start migration', required=True)
parser.add_argument('--enddate', type=str, help='Date from which endi migration', required=True)
parser.add_argument('--batchsize', type=int, help='The size of the batch to be migrated', required=False)
args = parser.parse_args()
mongo_uri = args.connstr
last_created = args.startdate if args.startdate else "2025-01-01"   
end_date = args.enddate if args.enddate else last_created + "T23:59:59"   
batch_size = args.batchsize if args.batchsize else 50

# Defining log file
log_filename = f"./runs/pk_migration_{last_created}-{end_date}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    filemode='w', 
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger()

# Connecting to client
client = MongoClient(mongo_uri)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

total_updated = 0
last_id = ""
try:

    # Starting execution
    log.info(f"Executing migration for batches of [{batch_size}] elements in date range [{last_created} - {end_date}]\n")
    while True:

        query = {}
            
        # Execute query using boundaries on created
        query = {"created": {"$gte": last_created, "$lte": end_date}}
        cursor = collection.find(query, sort=[("created", 1)], limit=batch_size)
        batch = list(cursor)
        if not batch or last_id == batch[0]["_id"]: # if query give no element or returns the same element of previous query, break the cicle!
            break
        requests = []

        log.info(f"Batch boundaries IDs: [{batch[0]["_id"]} ({batch[0]["created"]})] - [{batch[-1]["_id"]} ({batch[-1]["created"]})]")
            
        # Add each updated element in batch for write
        for event in batch:
            last_created = event["created"]
            if "PartitionKey" not in event:
                partition_key = event["created"][0:10]
                requests.append(UpdateOne({"_id": event["_id"]}, {"$set": {"PartitionKey": partition_key}}))
        last_id = batch[0]["_id"]

        # Execute update in bulk write
        if requests:
            try:
                result = collection.bulk_write(requests)
                total_updated += result.modified_count
                log.info(f"Updated {result.modified_count} events with newly generated PartitionKey fields.")

            except BulkWriteError as err:
                print("An error occurred during bulk_write:", err.details)
                log.info("An error occurred during bulk_write:", err.details)

    print(f"Total updated documents: {total_updated}")
    log.info(f"Total updated documents: {total_updated}")
    
except Exception as error:
    print("An error occurred during execution:", error.details)
    log.info("An error occurred during execution:", error.details)

