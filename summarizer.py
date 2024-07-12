from newspaper import Article
from googletrans import Translator
import nltk
import gradio as gr
import os
from datetime import datetime

nltk.download('punkt')

def translate_and_summarize(url, language, output_format):
    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        translator = Translator()
        art_title = translator.translate(article.title, dest=language)
        article_sum = translator.translate(article.summary, dest=language)
        
        if article.publish_date:
            publish_date_formatted = article.publish_date.strftime("%Y-%m-%d %I:%M:%S %p")
        else:
            publish_date_formatted = "Not available"

        output = f"Article Title:\n{art_title.text}\n\n"
        output += f"Article Summary:\n{article_sum.text}\n\n"
        output += f"Article Publish Date:\n{article.publish_date}\n\n"
        output += f"Article Image Link:\n{article.top_image}"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        base_filename = f"{datetime.now().strftime('%H-%M-%d-%m-%Y')}"

        if output_format == "HTML":
                html_filename = f"{base_filename}.html"
                with open("template.html", "r", encoding="utf-8") as template_file:
                    template = template_file.read()
                    html_content = template.replace("{{ article_title }}", art_title.text)\
                                        .replace("{{ article_summary }}", article_sum.text)\
                                        .replace("{{ article_image }}", article.top_image)\
                                        .replace("{{ page_creation_date }}", timestamp)
                with open(html_filename, "w", encoding="utf-8") as html_file:
                    html_file.write(html_content)
                return f"Summary saved as {html_filename}\n\n{output}"
        
        else:
            txt_filename = f"{base_filename}.txt"
            with open(txt_filename, "w", encoding="utf-8") as txt_file:
                txt_file.write(output)
            return f"Summary saved as {txt_filename}\n\n{output}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

iface = gr.Interface(
    fn=translate_and_summarize,
    inputs=[
        gr.Textbox(label="URL"),
        gr.Radio(["en", "hi"], label="Language", value="en"),
        gr.Radio(["HTML", "TXT"], label="Output Format", value="HTML")
    ],
    outputs="text",
    title="News Article Summary",
    description="Enter a news article URL and select a language and output format to get a translated summary. The summary will be saved as a text file or an HTML file.",
    css="custom_gradio.css"
)

iface.launch()
