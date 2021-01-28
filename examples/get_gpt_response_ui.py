#!/usr/bin/env python
# coding: utf-8

import os
import sys
import pandas as pd
from sqlalchemy import create_engine
import ipywidgets as widgets
from IPython.display import display
from IPython.display import update_display
from IPython.display import display_pretty

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
engine = create_engine(SQLALCHEMY_DATABASE_URI)

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from api import GPT, Example

#Define display flow for GPT question input
def on_button_clicked(b):
    def sql_button_clicked(b):
        df = pd.read_sql(query, engine)
        df_pretty = df.style.hide_index().set_properties(**{'background-color': 'black',
                               'color': 'lawngreen',
                               'border-color': 'white'})
        display(df_pretty)

    print ('\033[1mInput:\033[0m ' + inp.value)
    output = gpt.submit_request(inp.value)
    result = output['choices'][0].text
    query = result.split('output:')[1]
    print ('\033[1mGPT-3 Response:\033[0m ' + query)
    button2 = widgets.Button(description="Run SQL")
    button2.on_click(sql_button_clicked)
    display(button2)

#Construct GPT-3-instruct instance, add instruction and examples
gpt = GPT(engine="davinci-instruct-beta",
          temperature=0.3,
          max_tokens=200)
gpt.add_instruction('Given an input question, respond with syntactically correct PostgreSQL.')

gpt.add_example(Example('select columns from users table',
                        'select id, email, dt, plan_type, created_on, updated_on from users'))
gpt.add_example(Example('select columns from the charges table',
                        'select amount, amount_refunded, created, customer_id, status from charges'))
gpt.add_example(Example('select columns from the customers table',
                        'select created, email, id from customers'))

#Display UI to give GPT-3 prompt and run and display resulting SQL
inp = widgets.Text(description='Ask GPT-3:')
button1 = widgets.Button(description="Get GPT-3 Response")
Box = widgets.HBox([inp, button1])
print ('\033[1mInstruction:\033[0m ' + gpt.get_instruction_text())
button1.on_click(on_button_clicked)
display(Box)


