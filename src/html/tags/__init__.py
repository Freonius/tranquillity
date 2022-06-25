from typing import Dict, Type
from ._interface import IHtmlElement, Text


class A(IHtmlElement):
    pass


class Abbr(IHtmlElement):
    pass


class Address(IHtmlElement):
    pass


class Area(IHtmlElement):
    pass


class Article(IHtmlElement):
    pass


class Aside(IHtmlElement):
    pass


class Audio(IHtmlElement):
    pass


class B(IHtmlElement):
    pass


class Base(IHtmlElement):
    pass


class Basefont(IHtmlElement):
    pass


class Bdi(IHtmlElement):
    pass


class Bdo(IHtmlElement):
    pass


class Big(IHtmlElement):
    pass


class Blink(IHtmlElement):
    pass


class Blockquote(IHtmlElement):
    pass


class Body(IHtmlElement):
    pass


class Br(IHtmlElement):
    pass


class Button(IHtmlElement):
    pass


class Canvas(IHtmlElement):
    pass


class Caption(IHtmlElement):
    pass


class Center(IHtmlElement):
    pass


class Cite(IHtmlElement):
    pass


class Code(IHtmlElement):
    pass


class Col(IHtmlElement):
    pass


class Colgroup(IHtmlElement):
    pass


class Comment(IHtmlElement):
    pass


class Datalist(IHtmlElement):
    pass


class Dd(IHtmlElement):
    pass


class Del(IHtmlElement):
    pass


class Details(IHtmlElement):
    pass


class Dfn(IHtmlElement):
    pass


class Dialog(IHtmlElement):
    pass


class Dir(IHtmlElement):
    pass


class Div(IHtmlElement):
    pass


class Dl(IHtmlElement):
    pass


class Dt(IHtmlElement):
    pass


class Em(IHtmlElement):
    pass


class Embed(IHtmlElement):
    pass


class Fieldset(IHtmlElement):
    pass


class Figcaption(IHtmlElement):
    pass


class Figure(IHtmlElement):
    pass


class Font(IHtmlElement):
    pass


class Footer(IHtmlElement):
    pass


class Form(IHtmlElement):
    pass


class Frame(IHtmlElement):
    pass


class Framset(IHtmlElement):
    pass


class H1(IHtmlElement):
    pass


class H2(IHtmlElement):
    pass


class H3(IHtmlElement):
    pass


class H4(IHtmlElement):
    pass


class H5(IHtmlElement):
    pass


class H6(IHtmlElement):
    pass


class Head(IHtmlElement):
    pass


class Header(IHtmlElement):
    pass


class Hr(IHtmlElement):
    pass


class Html(IHtmlElement):
    pass


class I(IHtmlElement):
    pass


class Iframe(IHtmlElement):
    pass


class Img(IHtmlElement):
    pass


class Input(IHtmlElement):
    pass


class Ins(IHtmlElement):
    pass


class Kbd(IHtmlElement):
    pass


class Keygen(IHtmlElement):
    pass


class Label(IHtmlElement):
    pass


class Legend(IHtmlElement):
    pass


class Li(IHtmlElement):
    pass


class Link(IHtmlElement):
    pass


class Main(IHtmlElement):
    pass


class Map(IHtmlElement):
    pass


class Mark(IHtmlElement):
    pass


class Menu(IHtmlElement):
    pass


class Menuitem(IHtmlElement):
    pass


class Meta(IHtmlElement):
    pass


class Meter(IHtmlElement):
    pass


class Nav(IHtmlElement):
    pass


class Noframes(IHtmlElement):
    pass


class Noscript(IHtmlElement):
    pass


class Object(IHtmlElement):
    pass


class Ol(IHtmlElement):
    pass


class Optgroup(IHtmlElement):
    pass


class Option(IHtmlElement):
    pass


class Output(IHtmlElement):
    pass


class P(IHtmlElement):
    pass


class Param(IHtmlElement):
    pass


class Pre(IHtmlElement):
    pass


class Progress(IHtmlElement):
    pass


class Q(IHtmlElement):
    pass


class Rp(IHtmlElement):
    pass


class Rt(IHtmlElement):
    pass


class Ruby(IHtmlElement):
    pass


class S(IHtmlElement):
    pass


class Samp(IHtmlElement):
    pass


class Script(IHtmlElement):
    pass


class Section(IHtmlElement):
    pass


class Select(IHtmlElement):
    pass


class Small(IHtmlElement):
    pass


class Source(IHtmlElement):
    pass


class Span(IHtmlElement):
    pass


class Strike(IHtmlElement):
    pass


class Strong(IHtmlElement):
    pass


class Style(IHtmlElement):
    pass


class Sub(IHtmlElement):
    pass


class Summary(IHtmlElement):
    pass


class Sup(IHtmlElement):
    pass


class Table(IHtmlElement):
    pass


class Tbody(IHtmlElement):
    pass


class Td(IHtmlElement):
    pass


class Tfoot(IHtmlElement):
    pass


class Th(IHtmlElement):
    pass


class Thead(IHtmlElement):
    pass


class Time(IHtmlElement):
    pass


class Title(IHtmlElement):
    pass


class Tr(IHtmlElement):
    pass


class Track(IHtmlElement):
    pass


class Tt(IHtmlElement):
    pass


class U(IHtmlElement):
    pass


class Ul(IHtmlElement):
    pass


class Var(IHtmlElement):
    pass


class Video(IHtmlElement):
    pass


ALL_TAGS: Dict[str, Type[IHtmlElement]] = {
    'a': A,
    'abbr': Abbr,
    'address': Address,
    'area': Area,
    'article': Article,
    'aside': Aside,
    'audio': Audio,
    'b': B,
    'base': Base,
    'basefont': Basefont,
    'bdi': Bdi,
    'bdo': Bdo,
    'big': Big,
    'blink': Blink,
    'blockquote': Blockquote,
    'body': Body,
    'br': Br,
    'button': Button,
    'canvas': Canvas,
    'caption': Caption,
    'center': Center,
    'cite': Cite,
    'code': Code,
    'col': Col,
    'colgroup': Colgroup,
    'comment': Comment,
    'datalist': Datalist,
    'dd': Dd,
    'del': Del,
    'details': Details,
    'dfn': Dfn,
    'dialog': Dialog,
    'dir': Dir,
    'div': Div,
    'dl': Dl,
    'dt': Dt,
    'em': Em,
    'embed': Embed,
    'fieldset': Fieldset,
    'figcaption': Figcaption,
    'figure': Figure,
    'font': Font,
    'footer': Footer,
    'form': Form,
    'frame': Frame,
    'framset': Framset,
    'h1': H1,
    'h2': H2,
    'h3': H3,
    'h4': H4,
    'h5': H5,
    'h6': H6,
    'head': Head,
    'header': Header,
    'hr': Hr,
    'html': Html,
    'i': I,
    'iframe': Iframe,
    'img': Img,
    'input': Input,
    'ins': Ins,
    'kbd': Kbd,
    'keygen': Keygen,
    'label': Label,
    'legend': Legend,
    'li': Li,
    'link': Link,
    'main': Main,
    'map': Map,
    'mark': Mark,
    'menu': Menu,
    'menuitem': Menuitem,
    'meta': Meta,
    'meter': Meter,
    'nav': Nav,
    'noframes': Noframes,
    'noscript': Noscript,
    'object': Object,
    'ol': Ol,
    'optgroup': Optgroup,
    'option': Option,
    'output': Output,
    'p': P,
    'param': Param,
    'pre': Pre,
    'progress': Progress,
    'q': Q,
    'rp': Rp,
    'rt': Rt,
    'ruby': Ruby,
    's': S,
    'samp': Samp,
    'script': Script,
    'section': Section,
    'select': Select,
    'small': Small,
    'source': Source,
    'span': Span,
    'strike': Strike,
    'strong': Strong,
    'style': Style,
    'sub': Sub,
    'summary': Summary,
    'sup': Sup,
    'table': Table,
    'tbody': Tbody,
    'td': Td,
    'tfoot': Tfoot,
    'th': Th,
    'thead': Thead,
    'time': Time,
    'title': Title,
    'tr': Tr,
    'track': Track,
    'tt': Tt,
    'u': U,
    'ul': Ul,
    'var': Var,
    'video': Video,
}
