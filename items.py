import enum


class Global:

    def __init__(self, name="", title="", description=""):
        self.name = name
        self.title = title
        self.description = description

    def get_name(self):
        return self.name

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description


class Global_var(Global):

    def __init__(self, name="var", type_=""):
        super().__init__(name)
        self.type_ = type_

    def get_type(self):
        return self.type_

    def set_type(self, type_):
        self.type_ = type_


class Global_const(Global):

    def __init__(self, name="const", value=""):
        super().__init__(name)
        self.value = value

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value


class Function(Global):
    def __init__(self, name="func", return_type="", source_body=[]):
        super().__init__(name)
        self.return_type = return_type
        self.source_body = source_body
        self.parameters = []  # list of elements with type Global_var

    def add_parameter(self, parameter):
        self.parameters.append(parameter)

    def set_parameters(self, parameters):
        self.parameters = parameters

    def find_by_param_name(self, param_name):
        for param in self.parameters:
            if param.get_name() == param_name:
                return param
        return None

    def get_parameters(self):
        return self.parameters

    def set_return_type(self, return_type):
        self.return_type = return_type

    def get_return_type(self):
        return self.return_type

    def set_source_body(self, source_body):
        self.source_body = source_body

    def get_source_body(self):
        return self.source_body

    def process_docblock(self, docblock):

        tg_return = docblock.get_tags_by_name('@return')
        if tg_return is not None:
            self.return_type = tg_return[0].get_type()

        tgs_param = docblock.get_tags_by_name('@param')
        if tgs_param is not None:
            for tg_param in tgs_param:
                param = self.find_by_param_name(tg_param.get_name())
                if param is not None:
                    param.set_type(tg_param.get_type())

    def source_body_html(self):
        sb = ""
        for ln in self.source_body:
            sb += ln + '<br>'
        return sb


class Class(Global):
    def __init__(self, name, namespace, extends='', implements=''):
        super().__init__(name)
        self.namespace = namespace
        self.extends = extends
        self.implements = implements
        self.constants = []
        self.properties = []
        self.methods = []

    def get_namespace(self):
        return self.namespace

    def add_constant(self, constant):
        self.constants.append(constant)

    def add_property(self, __property):
        self.properties.append(__property)

    def add_method(self, method):
        self.methods.append(method)

    def get_constants(self):
        return self.constants

    def get_constants_with_mode(self, mod):
        return [const for const in self.constants if const.get_mod() == mod]

    def get_properties(self):
        return self.properties

    def get_properties_with_mode(self, mod):
        return [__property for __property in self.properties if __property.get_mod() == mod]

    def get_methods(self):
        return self.methods

    def get_methods_with_mode(self, mod):
        return [method for method in self.methods if method.get_mod() == mod]

    def get_inherited_class(self):
        return self.extends

    def get_inherited_interface(self):
        return self.implements


class Interface(Global):
    def __init__(self, name, namespace, parents=[]):
        super().__init__(name)
        self.namespace = namespace
        self.parents = parents
        # Only public constants and public methods
        self.constants = []
        self.methods = []

    def get_namespace(self):
        return self.namespace

    def add_constant(self, constant):
        self.constants.append(constant)

    def get_constants(self):
        return self.constants

    def set_constants(self, constants):
        self.constants = constants

    def add_method(self, method):
        self.methods.append(method)

    def set_methods(self, methods):
        self.methods = methods

    def get_methods(self):
        return self.methods

    def add_parent(self, parent):
        self.parents.append(parent)

    def set_parents(self, parents):
        self.parents = parents

    def get_parents(self):
        return self.parents


class Trait(Global):

    def __init__(self, name, namespace):
        super().__init__(name)
        self.namespace = namespace
        self.properties = []
        self.methods = []

    def get_namespace(self):
        return self.namespace

    def add_property(self, __property):
        self.properties.append(__property)

    def add_method(self, method):
        self.methods.append(method)

    def get_properties(self):
        return self.properties

    def get_properties_with_mode(self, mod):
        return [__property for __property in self.properties if __property.get_mod() == mod]

    def get_methods(self):
        return self.methods

    def get_methods_with_mode(self, mod):
        return [method for method in self.properties if method.get_mod() == mod]


class AccessModifier(enum.Enum):
    public = 1
    protected = 2
    private = 3


class Item(Global):

    def __init__(self, name, mod, title="", description=""):
        super().__init__(name, title, description)
        self.mod = mod

    def get_mod(self):
        return self.mod


class Property(Item):

    def __init__(self, name, mode, __type=""):
        super().__init__(name, mode)
        self.__type = __type

    def set_type(self, __type):
        self.__type = __type

    def get_type(self):
        return self.__type

    def process_docblock(self, docblock):

        tgs_var = docblock.get_tags_by_name('@var')
        if tgs_var is not None:
            for tg_var in tgs_var:
                if tg_var.get_name() == self.get_name():
                    self.set_type(tg_var.get_type())


class Const(Item):

    def __init__(self, name, mod, value):
        super().__init__(name, mod)
        self.value = value

    def get_value(self):
        return self.value


class Method(Item):
    def __init__(self, name, mod, return_type="", source_body=[]):
        super().__init__(name, mod)
        self.return_type = return_type
        self.source_body = source_body
        self.parameters = []

    def add_parameter(self, parameter):
        self.parameters.append(parameter)

    def set_parameters(self, parameters):
        self.parameters = parameters

    def get_parameters(self):
        return self.parameters

    def find_by_param_name(self, param_name):
        for param in self.parameters:
            if param.get_name() == param_name:
                return param
        return None

    def set_return_type(self, return_type):
        self.return_type = return_type

    def get_return_type(self):
        return self.return_type

    def set_source_body(self, source_body):
        self.source_body = source_body

    def get_source_body(self):
        return self.source_body

    def process_docblock(self, docblock):

        tg_return = docblock.get_tags_by_name('@return')
        if tg_return is not None:
            self.return_type = tg_return[0].get_type()

        tgs_param = docblock.get_tags_by_name('@param')
        if tgs_param is not None:
            for tg_param in tgs_param:
                param = self.find_by_param_name(tg_param.get_name())
                if param is not None:
                    param.set_type(tg_param.get_type())

    def source_body_html(self):
        sb = ""
        for ln in self.source_body:
            sb += ln + '<br>'
        return sb


class Namespace(Global):

    def __init__(self, name, parent_namespace=None, filename='', curpath=''):
        super().__init__(name)
        self.parent_namespace = parent_namespace
        self.curpath = curpath
        self.filename = filename
        self.global_vars = []
        self.constants = []
        self.child_namespaces = []
        self.functions = []
        self.classes = []
        self.interfaces = []
        self.traits = []
        self.file_author_name = ''
        self.file_author_email = ''

    def get_parent_namespace(self):
        return self.parent_namespace

    def get_root_namespace(self):
        cur_nm = self
        while cur_nm.parent_namespace is not None:
            cur_nm = cur_nm.parent_namespace
        return cur_nm

    def get_curpath(self):
        return self.curpath

    def get_filename(self):
        return self.filename

    def get_link(self):
        cur_nm = self
        link = ''
        while cur_nm is not None:
            cur_name = 'namespaces' + '\\'
            cur_name += cur_nm.get_name() if cur_nm.get_name() != '/' else 'root_nm'
            link = ('\\' if cur_nm.parent_namespace is not None and cur_nm.parent_namespace.get_name() != '' else '') + cur_name + link
            cur_nm = cur_nm.parent_namespace
        return link

    def add_global_var(self, var):
        self.global_vars.append(var)

    def get_global_vars(self):
        return self.global_vars

    def add_constants(self, constant):
        self.constants.append(constant)

    def get_constants(self):
        return self.constants

    def add_function(self, function):
        self.functions.append(function)

    def get_functions(self):
        return self.functions

    def add_class(self, __class):
        self.classes.append(__class)

    def get_classes(self):
        return self.classes

    def add_interface(self, interface):
        self.interfaces.append(interface)

    def get_interfaces(self):
        return self.interfaces

    def add_trait(self, trait):
        self.traits.append(trait)

    def get_traits(self):
        return self.traits

    def get_child_namespaces(self):
        return self.child_namespaces

    def get_namespace_name_ind(self, nm_name):
        ind = 0
        for nm in self.child_namespaces:
            if nm.get_name() == nm_name:
                return ind
            else:
                ind += 1
        return None

    def add_namespace(self, nm_name):
        nms = str.split(nm_name, '\\')
        cur_nm = self
        for nm in nms:
            try:
                tmp_nm_ind = cur_nm.get_namespace_name_ind(nm)
            except ValueError:
                tmp_nm_ind = None
            if tmp_nm_ind is not None:
                cur_nm = cur_nm.get_child_namespaces()[tmp_nm_ind]
            else:
                cur_nm.get_child_namespaces().append(Namespace(nm, cur_nm, cur_nm.get_filename(), cur_nm.get_curpath()))
                cur_nm = cur_nm.get_child_namespaces()[len(cur_nm.child_namespaces) - 1]
        return cur_nm

    def get_namespace(self, nm_name):
        nms = str.split(nm_name, '/')
        cur_nm = self
        for nm in nms:
            try:
                tmp_nm_ind = cur_nm.get_namespace_name_ind(nm)
            except ValueError:
                tmp_nm_ind = None
            if tmp_nm_ind is not None:
                cur_nm = cur_nm.get_child_namespaces()[tmp_nm_ind]
            else:
                return
        return cur_nm

    def process_docblock(self, docblock):
        tg_author = docblock.get_tags_by_name('@author')
        if tg_author is not None:
            self.file_author_name = tg_author[0].get_author_name()
            self.file_author_email = tg_author[0].get_author_email()


if __name__ == '__main__':
    # my_function = Function('func', AccessModifier.public,
    #                      [Var('var1', AccessModifier.private), Var('var2', AccessModifier.protected)])
    # li = [var for var in my_function.get_parameters() if var.get_mod() == AccessModifier.private]
    # for i in li:
    #   print(i.get_name())
    nm = Namespace('/', 'f2.php')
    nm.add_namespace('nm/mn/fuck')
    nm.add_namespace('nm/kz')
    ans = nm.get_namespace('nm/kz')
    if ans:
        print(ans.nm_name)
    else:
        print('Not found')
