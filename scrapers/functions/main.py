from firebase_functions import scheduler_fn, https_fn
from firebase_admin import initialize_app, firestore
from scraper_code.utils import getBCVUpdate, getParaleloUpdates

initialize_app()

## Cloud Functions Code
@scheduler_fn.on_schedule(schedule='0 */3 * * *', region='us-east4')
def update_bcv(req: https_fn.Request) -> https_fn.Response:
    """Check for updates from BCV every 3 hours"""

    # Initialize db and collection
    db = firestore.client()
    bcv_collection = db.collection('bcv')

    # Retrieve new Update
    update = getBCVUpdate()
    print(update)
    if not update:
        return https_fn.Response("Rate could not be updated.", 400)
    
    doc_id = update["unique_name"]

    # Look for update with doc_id
    doc = bcv_collection.document(doc_id).get()

    if doc.exists:
        # Update already exists
        return https_fn.Response("Update already exists!", 400)

    # Update added
    bcv_collection.document(doc_id).set(update)
    return https_fn.Response("Update Added.", 200)

@scheduler_fn.on_schedule(schedule='0 9,13,15 * * *', region='us-east4')
def update_paralelo(req: https_fn.Request) -> https_fn.Response:
    """Check for updates from Enparalelo at hour 9, 13 and 15"""

    # Initialize db and collection
    db = firestore.client()
    paralelo_collection = db.collection('paralelo')

    # Retrieve new Update
    updates = getParaleloUpdates()
    print(updates)
    if not updates:
        return https_fn.Response("Rate could not be updated.", 400)

    n_updates = 0
    for update in updates:
    
        doc_id = update["unique_name"]

        # Look for update with doc_id
        doc = paralelo_collection.document(doc_id).get()
        if doc.exists:
            # Update already exists, skip it
            continue

        # Update added
        paralelo_collection.document(doc_id).set(update)
        n_updates += 1

    print(n_updates)
    return https_fn.Response(f"Added {n_updates} updates.", 200)