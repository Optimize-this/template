
from streamlit_extras.add_vertical_space import add_vertical_space

from langchain.chat_models.gigachat import GigaChat
from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from langchain_community.vectorstores.docarray import DocArrayInMemorySearch
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type

from langchain.agents import (
    AgentExecutor,
    create_gigachat_functions_agent,
)
from langchain.agents.gigachat_functions_agent.base import (
    format_to_gigachat_function_messages,
)



model = GigaChat(
    #credentials=os.getenv("CREDENTIALS"),
    credentials=*****",#os.getenv("CREDENTIALS"),
    scope='GIGACHAT_API_CORP',
    verify_ssl_certs=False,
)



class FillingOutDocumentationInput(BaseModel):
    teg: str = Field(description="используемый тег")
    text_line: str = Field(description="искомый текст")


class FillingOutDocumentationTool(BaseTool):
    name = "filling_out_documentation"
    description = """Выполняет заполнение шаблона документа.
    
    Пример. Нужно внести в шаблон текст {teg: #text1#, text_line: текст}"""

    args_schema: Type[BaseModel] = FillingOutDocumentationInput

    def _run(self, teg: str, text_line: str) -> str:
        
        print(f"найденный ответ для {teg}: {text_line}")
        #подумать над добавлением проверки возвращенного ответа
        #if not years:
        #    return "Уточни на какой срок ипотека. И вызови эту функцию снова"

        res = (
            f"сообщи, что внес в документ {text_line}"
        )
        return res



def put_in_word(teg, text):
    import docx

    # Путь к файлу Word
    file_path = 'template.docx'

    # Открытие файла Word
    doc = docx.Document(file_path)

    # Поиск всех текстовых элементов в документе
    for paragraph in doc.paragraphs:
        # Проверка, содержит ли параграф тег #int
        #if teg in paragraph.text:
            # Вставка текста перед тегом #int
        #    paragraph.text = paragraph.text.replace(teg, text)


        if paragraph.text.find(teg)>=0:
                paragraph.text=paragraph.text.replace(teg, text)


    # Сохранение изменений в файле
    doc.save(file_path)

    # Закрытие файла
    #doc.close()




tools = []
agent = create_gigachat_functions_agent(model, tools)

# AgentExecutor создает среду, в которой будет работать агент
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=False, return_intermediate_steps=True
)

requests={
    '#text1#': 'изложи научную составляющую научной темы в контексте. Ответ занеси в  шаблон документа. ',
    '#text2#':'сформулируй Научная новизна научной темы, значение для развития соответствующего направления (направлений) фундаментальных, поисковых, прикладных исследований, экспериментальных разработок. Ответ занеси в  шаблон документа.',
    '#text3#':'сформулируй Научное и научно-техническое сотрудничество, в том числе международное, в рамках научной темы (участие в международных и российских исследовательских программах, проектах, научных коллаборациях и консорциумах физических лиц и организаций и иные формы сотрудничества) (заполняется при наличии). Ответ занеси в  шаблон документа.',
    '#text4#':'сформулируй Достижимость заявленных в научной теме результатов и показателей с учетом оценки кадрового потенциала. Ответ занеси в  шаблон документа.',
    '#text5#':'сформулируй Потенциал практического применения ожидаемых научных и научно-технических результатов, в том числе с учетом приоритетов Стратегии научно-технологического развития Российской Федерации, утвержденной Указом Президента Российской Федерации от 1 декабря 2016 г. № 642. Обязательная фраза: Тема соответствует п. 20, подпункт «в» СНТР «Переход к персонализированной медицине, высокотехнологичному здравоохранению и технологиям здоровьесбережения, в том числе за счет рационального применения лекарственных препаратов (прежде всего антибактериальных)» Ответ занеси в  шаблон документа.',
}


def call_FillingOutDocumentationTool():

    
    
    
    with open("example.txt", "r", encoding="utf-8") as file:
        description = file.read()
    
    
    system_FillingOutDocumentation = f"""Ты эксперт в медицине. 
    Тебе нужно проанализировать представленный документ и дать научную оценку.
    Вот анализируемая статья: {description}
    """ 
    chat_history = [SystemMessage(content=system_FillingOutDocumentation)]




    for key, req in requests.items():
        
        print(f"Ищем: {req}")
        if req == "":
            break
        result = agent_executor.invoke(
            {
                "chat_history": chat_history,
                "input": req,
            }
        )
        print("\n")
        print("\033[93m" + f"Bot: {result['output']}" + "\033[0m")
        
        put_in_word(key, result["output"])

        chat_history.append(HumanMessage(content=req))
        chat_history += format_to_gigachat_function_messages(result["intermediate_steps"])
        chat_history.append(AIMessage(content=result["output"]))



if __name__ == '__main__':
    call_FillingOutDocumentationTool()
    #main()
