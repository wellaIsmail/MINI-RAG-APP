import os

class TemplateParser:
    def __init__(self, language: str=None, default_language:str ='en'):
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.default_language = default_language
        self.language = None
        self.language = self.set_language(language=language)


    def set_language(self, language:str):
        if not language:
            self.language = self.default_language
        language_path = os.path.join(self.current_path,"locales",language)
        if os.path.exists(language_path):
            self.language = language
        else:
            self.language = self.default_language
        # lang = language or self.default_language
        # folder = os.path.join(self.current_path, "locales", lang)
        # if os.path.isdir(folder):
        #     return lang
        # return self.default_language
        return self.language

    def get(self, group:str, key:str, vars:dict={}):
        if not group or not key:
            return None
        group_path = os.path.join(self.current_path,"locales",self.language,f"{group}.py")
        targeted_language = self.language
        if not os.path.exists(group_path):
            group_path = os.path.join(self.current_path,"locales",self.default_language,f"{group}.py")
            targeted_language = self.default_language
        if not os.path.exists(group_path):
            return None

       # Import group Module
        module = __import__(f"stores.llm.templates.locales.{targeted_language}.{group}",fromlist=[group])
        if not module:
            return None
        key_attribute = getattr(module, key)
        return key_attribute.substitute(vars)
