from flask import Flask, jsonify, request, url_for, abort
from service.models import Account
from service.common import status  # HTTP Status Codes
from service import app

@app.route("/health")
def health():
    """Health Check Endpoint"""
    return jsonify(status="OK"), status.HTTP_200_OK

@app.route("/")
def index():
    """Root URL"""
    return jsonify(name="DevOps Capstone Project", version="1.0.0")

@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")

    account = Account()
    account.deserialize(request.get_json())
    account.create()
    app.logger.info("Account with ID [%s] created.", account.id)

    location_url = url_for("get_account", account_id=account.id, _external=True)
    return jsonify(account.serialize()), status.HTTP_201_CREATED, {"Location": location_url}

@app.route("/accounts", methods=["GET"])
def list_accounts():
    """Returns all of the Accounts"""
    app.logger.info("Request to list Accounts")
    accounts = Account.all()
    results = [account.serialize() for account in accounts]
    return jsonify(results), status.HTTP_200_OK

@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    """
    Retrieve a single Account
    """
    app.logger.info("Request to retrieve Account with ID: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id '{account_id}' was not found.")
    return jsonify(account.serialize()), status.HTTP_200_OK

@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """
    Update an Account
    """
    app.logger.info("Request to update Account with ID: %s", account_id)
    check_content_type("application/json")
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id '{account_id}' was not found.")

    account.deserialize(request.get_json())
    account.update()
    return jsonify(account.serialize()), status.HTTP_200_OK

@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """
    Delete an Account
    """
    app.logger.info("Request to delete Account with ID: %s", account_id)
    account = Account.find(account_id)
    if account:
        account.delete()
    return "", status.HTTP_204_NO_CONTENT

def check_content_type(content_type):
    """Checks that the media type is correct"""
    if request.headers["Content-Type"] != content_type:
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}"
        )
