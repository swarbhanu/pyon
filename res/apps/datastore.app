name: datastore
description: Data store service
version: 0.1
processapp: [prototype.datastore_service, DataStoreService]
config:
    type: MockDB
    forceClean: false