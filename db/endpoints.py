import os
from user_group import create_and_upload
from manage_users import update_users_json, create_users_json, update_id_json

def create_new_user(phone_number, core_data):
    result = create_and_upload(phone_number, core_data)

    group_id, core_id, core_cid, index_id, index_cid = result

    print(group_id, core_id, core_cid, index_id, index_cid)

    update_users_json(phone_number, group_id, core_id, core_cid, index_id, index_cid)

def setup_db():
    id = create_users_json({})
    update_id_json(id)

# Testing
if __name__ == "__main__":
    setup_db()
    # create_new_user("2247707887", {"keys": "values"})

