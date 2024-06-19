import streamlit as st

# Initialize session state to store the list of inputs and the index of the item being edited
if "texts" not in st.session_state:
    st.session_state.texts = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = -1


def add_text():
    user_input = st.session_state.user_input
    if user_input:
        st.session_state.texts.append(user_input)
        st.session_state.user_input = ""  # Clear the input field


def update_text(index):
    st.session_state.texts[index] = st.session_state.edit_input
    st.session_state.edit_index = -1
    st.session_state.edit_input = ""  # Clear the edit input field


def edit_text(index):
    st.session_state.edit_index = index
    st.session_state.edit_input = st.session_state.texts[index]


def export_list():
    # Create a string with each text on a new line
    text_list = "\n".join(st.session_state.texts)
    return text_list


st.title("A Glossary for Research on Human Crowd Dynamics – 2nd Edition.")

# Input text field
st.text_input("Enter new concept:", key="user_input", on_change=add_text)

# Display the list of texts with edit buttons
st.write("### List of Texts:")
for i, text in enumerate(st.session_state.texts):
    if st.session_state.edit_index == i:
        st.text_input("Edit text:", value=st.session_state.edit_input, key="edit_input")
        st.button("Save", on_click=update_text, args=(i,))
        st.button(
            "Cancel", on_click=lambda: setattr(st.session_state, "edit_index", -1)
        )
    else:
        st.write(f"- {text}")
        st.button("Edit", key=f"edit_{i}", on_click=edit_text, args=(i,))


# Add a button to export the list as a .txt file
exported_text = export_list()
st.sidebar.download_button(
    label=":floppy_disk: Export list",
    data=exported_text,
    file_name="list_concepts.txt",
    mime="text/plain",
)
