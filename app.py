import streamlit as st
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
save = st.sidebar.empty()
msg = st.sidebar.empty()

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
        logger.info(f"Added new concept: {user_input}")
        st.info(f"Added new concept: {user_input}")


def update_text(index):
    original_text = st.session_state.texts[index]
    updated_text = st.session_state.edit_input
    st.session_state.texts[index] = updated_text
    st.session_state.edit_index = -1
    st.session_state.edit_input = ""  # Clear the edit input field
    logger.info(f"Updated concept from '{original_text}' to '{updated_text}'")


def edit_text(index):
    st.session_state.edit_index = index
    st.session_state.edit_input = st.session_state.texts[index]
    logger.info(f"Editing concept: {st.session_state.edit_input}")


def export_list():
    # Create a string with each text on a new line
    text_list = "\n".join(st.session_state.texts)
    logger.info("Exported list of concepts")
    return text_list


def main():
    st.title("A Glossary for Research on Human Crowd Dynamics – 2nd Edition.")

    # Input text field
    st.text_input("Enter new concept:", key="user_input", on_change=add_text)

    # Display the list of texts with edit buttons
    st.write("### List of concepts:")
    c1, c2 = st.columns(2)
    for i, text in enumerate(st.session_state.texts):
        if st.session_state.edit_index == i:
            st.text_input(
                "Edit text:", value=st.session_state.edit_input, key="edit_input"
            )
            st.button("Save", on_click=update_text, args=(i,))
            st.button(
                "Cancel", on_click=lambda: setattr(st.session_state, "edit_index", -1)
            )
        else:
            c1.write(f"- {text}")
            c2.button("Edit", key=f"edit_{i}", on_click=edit_text, args=(i,))

    # Add a button to export the list as a .txt file
    exported_text = export_list()
    save.download_button(
        label=":floppy_disk: Export list",
        data=exported_text,
        file_name="list_concepts.txt",
        mime="text/plain",
    )


if __name__ == "__main__":
    main()
