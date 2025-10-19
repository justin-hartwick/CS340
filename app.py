# DASH Framework for Python Script
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import urllib.parse

# TODO: import for your CRUD module
from CRUD_Python_Module import AnimalShelter

# Build App
app = Dash(__name__)

app.layout = html.Div([
    # This element generates an HTML Heading with your name
    html.H1("Module 5 Assignment - Justin Hartwick"),
    
    # This Input statement sets up an Input field for the username.
    dcc.Input(
        id="input_user".format("text"),
        type="text",
        placeholder="input type {}".format("text")
    ),
    
    # This Input statement sets up an Input field for the password.
    # This designation masks the user input on the screen.
    dcc.Input(
        id="input_passwd".format("password"),
        type="password",
        placeholder="input type {}".format("password")
    ),
    
    # Create a button labeled 'Submit'. When the button is pressed
    # the n_clicks value will increment by 1. 
    html.Button('Submit', id='submit-val', n_clicks=0),
    
    # Generate a horizontal line separating our input from our
    # output element
    html.Hr(),
    
    # This sets up the output element for the dashboard. The
    # purpose of the stlye option is to make sure that the 
    # output will function like a regular text area and accept
    # newline ('\n') characters as line-breaks.
    html.Div(id="query-out", style={'whiteSpace': 'pre-line'})
    # TODO: insert unique identifier code here. Please Note: 
    # when you insert another HTML element here, you will need to 
    # add a comma to the previous line.
])

# Define callback to update output-block
# NOTE: While the name of the callback function doesn't matter,
# the order of the parameters in the callback function are the
# same as the order of Input methods in the @app.callback
# For the callback function below, the callback is grabbing the
# information from the input_user and input_password entries, and
# then the value of the submit button (has it been pressed?)
@app.callback(
    Output('query-out', 'children'),
    [
        Input('input_user', 'value'),
        Input('input_passwd', 'value'),
        Input(component_id='submit-val', component_property='n_clicks')
    ]
)
def update_output(inputUser, inputPass, n_clicks):
    if n_clicks > 0:
        try:
            # Encode username and password for safe URL use
            username = urllib.parse.quote_plus(inputUser)
            password = urllib.parse.quote_plus(inputPass)

            # TODO: Instantiate CRUD object
            crud = AnimalShelter(username, password)

            # TODO: Return example query results
            results = crud.read({"animal_type": "Dog", "name": "Lucy"})
            output = ""
            count = 0
            for item in results:
                output += f"{item}\n"
                count += 1
                if count >= 3:
                    break  # Limit to first 3 results for display
            return output if output else "No results found."
        except Exception as e:
            return f"Connection failed or error occurred:\n{str(e)}"

# Run app
app.run(debug=True, host='0.0.0.0', port=8050)

