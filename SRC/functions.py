import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import ssl
import argparse
from clean import df_ff, df_ff_state_pop_income
from analysis import state_conclusion
import seaborn as sns
from fpdf import FPDF
import smtplib
import os
gmail_password = os.getenv("gmail_password")


def get_args(argv=None):
    valid_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
                    'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Northern Mariana Islands', 'Ohio', 'Oklahoma', 'Oregon', 'Palau', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
    valid_foodtypes = ['mexican', 'sandwich', 'italian', 'chicken', 'fish', 'asian',
                       'burger', 'ice cream', 'mediterranean', 'middle east', 'hot dog', 'american fast food']
    parser = argparse.ArgumentParser(
        description="Get USA state and fast food company name")
    parser.add_argument("--state", "-s", type=str,
                        choices=valid_states, help="USA State name", required=True)
    parser.add_argument("--fastfoodtype", "-f", type=str, choices=valid_foodtypes,
                        help="fast food type", required=True)
    return parser.parse_args(argv)


def ranking_avg_income(state):
    df_state_income = df_ff_state_pop_income.sort_values(
        by=['avg_income'], ascending=False).reset_index(drop=True)
    average_income = int(
        df_ff_state_pop_income[df_ff_state_pop_income.state == state]['avg_income'])
    return "{} is the state nº {} in average income (${})".format(state, df_state_income[df_state_income.state == state].index[0] + 1, average_income)


def ranking_ff_rest(state):
    df_state_ff_rest = df_ff_state_pop_income.sort_values(
        by=['ffrest_percapita'], ascending=False).reset_index(drop=True)
    return "{} is the state nº {} in number of fast food restaurants per capita (per 10K citizens)".format(state, df_state_ff_rest[df_state_ff_rest.state == state].index[0] + 1)


def ranking_ff_type(state, fastfoodtype):
    df_state_ff_type = df_ff[df_ff.categories == fastfoodtype].groupby(
        ['state'], as_index=False).count()
    df_state_ff_type.sort_values(
        by=['categories'], ascending=False).reset_index(drop=True)
    if len(df_state_ff_type[df_state_ff_type.state == state]) > 0:
        ranking = df_state_ff_type[df_state_ff_type.state ==
                                   state].index[0] + 1
        if ranking > 3:
            ranking = "{}th ".format(ranking)
        if ranking == 1:
            ranking = ""
        if ranking == 2:
            ranking = "second "
        if ranking == 3:
            ranking = "third "
        return "{} is the {}state with more {} restaurants in the US".format(state, ranking, fastfoodtype)
    return "{} has no {} restaurants (disclaimer: analysis done with a subset of the whole dataset - not available for free)".format(state, fastfoodtype)


def report_generator(state, fastfoodtype):
    return "- {}\n- {}\n{}\n- {}\n".format(ranking_avg_income(state), ranking_ff_rest(state), state_conclusion, ranking_ff_type(state, fastfoodtype))


def plot_generator(state, fastfoodtype):
    plot_df = df_ff_state_pop_income
    plot_df['USA_states'] = plot_df['state'].apply(
        lambda text: state if text == state else "Rest of States")
    plot = sns.lmplot(x="avg_income", y="ffrest_percapita", hue="USA_states", legend="full", fit_reg=False,
                      data=plot_df, palette="Paired")
    sns.regplot(x="avg_income", y="ffrest_percapita",
                data=plot_df, scatter=False, ax=plot.axes[0, 0])
    final_plot = plot.set_axis_labels(
        "Avg household income ($)", "# fast food restaurants (per 10K citizens)")
    final_plot.savefig("output.png")
    return final_plot


def pdf_generator(state, fastfoodtype):
    pdf = FPDF(format='letter', unit='in')
    pdf.l_margin = pdf.l_margin*4.0
    pdf.r_margin = pdf.r_margin*4.0
    pdf.t_margin = pdf.t_margin*4.0
    pdf.b_margin = pdf.b_margin*4.0
    pdf.add_page()

    effective_page_width = pdf.w - 2*pdf.l_margin

    epw = pdf.w - pdf.l_margin - pdf.r_margin
    eph = pdf.h - pdf.t_margin - pdf.b_margin

    pdf.set_font("helvetica", size=15)
    pdf.multi_cell(effective_page_width, 0.25,
                   'Relationship between the number of fast food companies and average household income')
    pdf.ln(0.30)

    my_text = report_generator(state, fastfoodtype)

    pdf.set_font('helvetica', 'B', 10.0)
    pdf.cell(1.0, 0.15, '{} analysis:'.format(state))
    pdf.ln(0.30)

    pdf.set_font('helvetica', '', 10.0)
    pdf.multi_cell(effective_page_width, 0.15, my_text)
    pdf.ln(0.30)

    plot_generator(state, fastfoodtype)
    pdf.image("output.png", w=pdf.w/2.0, h=pdf.h/4.0)
    pdf.ln(0.10)

    pdf.set_font("helvetica", 'I', size=8)
    pdf.multi_cell(effective_page_width, 0.15, "Figure 1: Relationship between the number of fast food companies and average household income in {}. Source: own elaboration from United States Census Bureau and Datafiniti".format(state))
    pdf.ln(0.25)

    pdf.output('report.pdf', 'F')


def email_generator(state, fastfoodtype):
    subject = "An email with attachment from Python"
    body = "This is an email with attachment sent from Python"
    sender_email = "bego.ironhack@gmail.com"
    receiver_email = input("Enter your email address to send you the report: ")
    password = gmail_password
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    pdf_generator(state, fastfoodtype)
    filename = "report.pdf"  # In same directory as script
    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    return print("Email sent to {}".format(receiver_email))
