import streamlit as st
import openai

if 'current_response' not in st.session_state:
    st.session_state.current_response = None

st.title('Skills Generator')

st.write("""
Input your details below and get top skills generated for your desired job title!
""")

api_key = st.text_input("OpenAI API Key", type="password")

job_title = st.text_input("job title", max_chars=60)
industry = st.text_area("Specify the industry or sector your interested?", max_chars=2000)
#model_color = st.slider("Creativity", 0.0, 1.0, 0.3, 0.05)
prompt_style = st.selectbox("Style", ["json", "bullets", "fancy", "table", "two paragraphs"])
gen_skill= st.button("Run")

def generate_prompt():
    result = f"""Provide me with top 10 hard skills and soft skills in demand for {job_title}: Make sure they are customized to the {industry} Industry"""
    #result += job_responsibility.strip() + "\n"

    #if prompt_style == "idea":
    #    result += "\nCan you suggest top hard and soft skills"
    #else:
    #    result += "\nWrite a job description with years of experience needed"

    if prompt_style == "bullets":
        result += " The format must be in bullet points."
    elif prompt_style == "json":
        result += " The format must be in json format"
    elif prompt_style == "table":
        result += " Table includes Hard skills and Soft Skills columns and their values"
    elif prompt_style == "fancy":
        result += " Use fancy words to make the skills look good."
    elif prompt_style == "two paragraphs":
        result += " Use at least two paragraphs for the description."

    return result.strip()

def generate_description(prompt):
    openai.api_key = api_key
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        #temperature=model_color,
        max_tokens=768,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response

input_prompt = generate_prompt()

if st.checkbox("Show prompt"):
    st.write(input_prompt)

if gen_skill:
    if not api_key:
        st.error("Please enter your OpenAI API key")
    elif not job_title or not industry:
        st.error("Please fill job title and industry")
    else:
        with st.spinner("Generating your skills..."):
            st.session_state.current_response = generate_description(input_prompt)
            st.success("Done!")

if st.session_state.current_response:
    st.write(st.session_state.current_response['choices'][0]['text'].replace("\n", "\n\n"))