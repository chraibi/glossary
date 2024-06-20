import streamlit as st
import logging
from sqlalchemy import create_engine, Column, Integer, Text, asc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configure logging to write to a file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Configure database
DATABASE_URL = "sqlite:///texts.db"
Base = declarative_base()


class TextItem(Base):
    __tablename__ = "texts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def num_items():
    return len(get_all_texts())


def get_all_texts():
    session = Session()
    texts = session.query(TextItem).order_by(asc(TextItem.content)).all()
    session.close()
    return [(text.id, text.content) for text in texts]


def add_text_to_db(content):
    session = Session()
    new_text = TextItem(content=content)
    session.add(new_text)
    session.commit()
    session.close()


def update_text_in_db(text_id, new_content):
    session = Session()
    text_item = session.query(TextItem).get(text_id)
    text_item.content = new_content
    session.commit()
    session.close()


def delete_text_from_db(text_id):
    session = Session()
    text_item = session.query(TextItem).get(text_id)
    session.delete(text_item)
    session.commit()
    session.close()


# Initialize session state to store the index of the item being edited
if "edit_index" not in st.session_state:
    st.session_state.edit_index = -1

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None


def add_text():
    user_input = st.session_state.user_input
    if user_input:
        add_text_to_db(user_input)
        st.session_state.user_input = ""  # Clear the input field
        logger.info(f"Added new concept: {user_input}")


def update_text():
    updated_text = st.session_state.edit_input
    text_id = st.session_state.edit_id
    if updated_text:
        update_text_in_db(text_id, updated_text)
        st.session_state.edit_index = -1
        st.session_state.edit_input = ""  # Clear the edit input field
        st.session_state.edit_id = None
        logger.info(f"Updated concept to '{updated_text}'")


def edit_text(index, text_id):
    st.session_state.edit_index = index
    st.session_state.edit_id = text_id
    st.session_state.edit_input = get_all_texts()[index][1]
    logger.info(f"Editing concept: {st.session_state.edit_input}")


def export_list():
    # Create a string with each text on a new line
    text_list = "\n".join([text[1] for text in get_all_texts()])
    logger.info("Exported list of concepts")
    return text_list


def main():
    st.title("A Glossary for Research on Human Crowd Dynamics – 2nd Edition.")
    st.link_button(
        "A Glossary for Research on Human Crowd Dynamics",
        "https://collective-dynamics.eu/index.php/cod/article/view/A19)",
    )
    st.write("-------------------")

    # Input text field
    st.text_input(
        ":arrow_forward: Enter new concept:", key="user_input", on_change=add_text
    )
    # Display the list of texts with edit buttons
    st.write("### :round_pushpin:  List of concepts:")
    texts = get_all_texts()
    c1, c2 = st.columns(2)
    for i, (text_id, text) in enumerate(texts):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            if st.session_state.edit_index == i:
                st.text_input(
                    "Edit text:", value=st.session_state.edit_input, key="edit_input"
                )
            else:
                st.write(f"- **{text}**")
        with col2:
            if st.session_state.edit_index == i:
                st.button("Save", on_click=update_text)
                st.button(
                    "Cancel",
                    on_click=lambda: setattr(st.session_state, "edit_index", -1),
                )
            else:
                st.button(
                    f"Edit", key=f"edit_{i}", on_click=edit_text, args=(i, text_id)
                )

        # if st.session_state.edit_index == i:
        #     st.text_input(
        #         "Edit text:", value=st.session_state.edit_input, key="edit_input"
        #     )
        #     st.button("Save", on_click=update_text)
        #     st.button(
        #         "Cancel", on_click=lambda: setattr(st.session_state, "edit_index", -1)
        #     )
        # else:
        #     c1.write(
        #         f"{i+1} - {text}",
        #         # disabled=True,
        #         # type="secondary",
        #     )
        #     c2.button(
        #         f"Edit {i+1}",
        #         key=f"edit_{i}",
        #         on_click=edit_text,
        #         args=(i, text_id),
        #         type="primary",
        #     )

    # Add a button to export the list as a .txt file
    exported_text = export_list()
    st.sidebar.download_button(
        label=":floppy_disk: Export list",
        data=exported_text,
        file_name="list_concepts.txt",
        mime="text/plain",
    )
    st.sidebar.write("-----------------------")
    st.sidebar.metric(":bar_chart: **Number of items**", value=num_items())


if __name__ == "__main__":
    main()
