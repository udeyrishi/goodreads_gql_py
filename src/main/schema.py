import graphene

class Book(graphene.ObjectType):
    title = graphene.NonNull(
        graphene.String, 
        description="The title of the book.", 
        resolver=lambda xml, info: xml.findall('title')[0].text
    )

    isbn = graphene.String(
        description="The ISBN of the book.", 
        resolver=lambda xml, info: xml.findall('isbn')[0].text
    )
    
    isbn13 = graphene.String(
        description="The ISBN13 of the book.", 
        resolver=lambda xml, info: xml.findall('isbn13')[0].text
    )

    authors = graphene.NonNull(
        graphene.List(lambda: Author),
        description="All the authors of this book."
    )

    @staticmethod
    async def resolve_authors(xml, info):
        author_ids = [int(author.findall('id')[0].text) for author in xml.findall('authors')[0].findall('author')]
        return await info.context['author_loader'].load_many(author_ids)

class Author(graphene.ObjectType):
    id = graphene.NonNull(
        graphene.Int, 
        description="The author's ID.", 
        resolver=lambda xml, info: int(xml.findall('id')[0].text)
    )
    
    name = graphene.NonNull(
        graphene.String, 
        description="The name of the author.", 
        resolver=lambda xml, info: xml.findall('name')[0].text
    )
    
    books = graphene.NonNull(
        graphene.List(Book), 
        description="All the books by the author.",
        resolver=lambda xml, info: xml.findall('books')[0].findall('book')
    )

class Query(graphene.ObjectType):
    author = graphene.Field(Author, id=graphene.NonNull(graphene.Int), description='An author.')
    
    @staticmethod
    async def resolve_author(_, info, id):
        return await info.context['author_loader'].load(id)

schema = graphene.Schema(query=Query)