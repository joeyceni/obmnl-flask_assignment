# Import libraries
from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

# Create operation: Display add transaction form
# Route to handle the creation of a new transaction
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Create a new transaction object using form field values
        transaction = {
            'id': len(transactions) + 1,            # Generate a new ID based on the current length of the transactions list
            'date': request.form['date'],           # Get the 'date' field value from the form
            'amount': float(request.form['amount']) # Get the 'amount' field value from the form and convert it to a float
        }
        # Append the new transaction to the transactions list
        transactions.append(transaction)

        # Redirect to the transactions list page after adding the new transaction
        return redirect(url_for("get_transactions"))
    
    # If the request method is GET, render the form template to display the add transaction form
    return render_template("form.html")


# Update operation: Display edit transaction form
# Route to handle the editing of an existing transaction
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']           # Get the 'date' field value from the form
        amount = float(request.form['amount'])# Get the 'amount' field value from the form and convert it to a float

        # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date       # Update the 'date' field of the transaction
                transaction['amount'] = amount   # Update the 'amount' field of the transaction
                break                            # Exit the loop once the transaction is found and updated

        # Redirect to the transactions list page after updating the transaction
        return redirect(url_for("get_transactions"))
    
    # If the request method is GET, find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            # Render the edit form template and pass the transaction to be edited
            return render_template("edit.html", transaction=transaction)

    # If the transaction with the specified ID is not found, handle this case (optional)
    return {"message": "Transaction not found"}, 404

# Delete operation: Delete a transaction
# Route to handle the deletion of an existing transaction
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from the list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)  # Remove the transaction from the transactions list
            break  # Exit the loop once the transaction is found and removed

    # Redirect to the transactions list page after deleting the transaction
    return redirect(url_for("get_transactions"))

# Search operation: Display transactions within a user specified range
# Route to handle the search of transactions within range
@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Create a new transaction object using form field values
        min_amount = request.form.get('min_amount')
        max_amount = request.form.get('max_amount')
        
        # Convert form data to floats; default to None if conversion fails
        min_amount = float(min_amount) if min_amount else None
        max_amount = float(max_amount) if max_amount else None

        # Filter transactions based on the amount range
        filtered_transactions = [
            transaction for transaction in transactions
            if (min_amount is None or transaction['amount'] >= min_amount) and
                (max_amount is None or transaction['amount'] <= max_amount)
        ]

        # Redirect to the transactions list page after adding the new transaction
        return render_template("transactions.html", transactions=filtered_transactions)
    
    # If the request method is GET, render the form template to display the add transaction form
    return render_template("search.html")

@app.route("/balance")
def total_balance():
    # Calculate the total balance by summing the amount values
    total = sum(transaction['amount'] for transaction in transactions)
    return render_template("transactions.html", transactions=transactions, balance=total)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)