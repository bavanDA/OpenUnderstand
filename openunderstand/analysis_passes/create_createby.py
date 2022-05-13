# expression -> NEW creator


"""
## Description
This module find all OpenUnderstand create and createby references in a Java project


## References


"""

__author__ = 'Parmida Majmasanaye , Zahra Momeninezhad , Bayan Divaani-Azar , Bavan Divaani-Azar'
__version__ = '0.1.0'

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
import analysis_passes.class_properties as class_properties


class CreateAndCreateByListener(JavaParserLabeledListener):

    def __init__(self):
        self.class_name = None
        self.package_name = None
        self.refers = {}
        self.create = []

    def get_refers(self):
        print(self.refers)
        return self.refers

    def get_create(self):
        return self.create

    def get_method_content(self, c):
        parents = ""
        content = ""
        current = c
        while current is not None:
            if type(current.parentCtx).__name__ == "ClassBodyDeclaration2Context":
                content = current.parentCtx.getText()
                break
                parents = (current.parentCtx.typeTypeOrVoid().getText())
            current = current.parentCtx

        print(f"Entity contex : {content}")

        return parents, content

    def get_method_modifiers(self, c):
        parents = ""
        modifiers = []
        current = c
        while current is not None:
            if "ClassBodyDeclaration" in type(current.parentCtx).__name__:
                parents = (current.parentCtx.modifier())
                break
            current = current.parentCtx
        for x in parents:
            if x.classOrInterfaceModifier():
                modifiers.append(x.classOrInterfaceModifier().getText())
        return modifiers

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.package_name = ctx.qualifiedName().getText()

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.class_name = ctx.IDENTIFIER().getText()

    def enterExpression4(self, ctx: JavaParserLabeled.Expression4Context):

        new_class_name = ctx.creator().createdName().IDENTIFIER()[0].getText()

        if not self.refers.__contains__(self.class_name):
            self.refers[self.class_name] = []
        self.refers[self.class_name].append(new_class_name)

        if ctx.creator().classCreatorRest():
            all_refs = class_properties.ClassPropertiesListener.findParents(ctx)
            [line, col] = str(ctx.start).split(",")[3].split(":")

            modifiers = self.get_method_modifiers(ctx)
            method_return, method_context = self.get_method_content(ctx)

            self.create.append(
                {"scope_name": all_refs[-1], "scope_longname": ".".join(all_refs), "scope_modifiers": modifiers,
                 "scope_return_type": method_return, "scope_content": method_context,
                 "line": line, "col": col[:-1], "refent": new_class_name,
                 "scope_parent": all_refs[-2] if len(all_refs) > 2 else None,
                 "potential_refent": ".".join(
                     all_refs[:-1]) + "." + new_class_name, "package_name": self.package_name})
