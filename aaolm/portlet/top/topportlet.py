from zope.interface import implements
from Acquisition import aq_inner

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from aaolm.portlet.top import TopPortletMessageFactory as _


class ITopPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    text_field = schema.Text(title=_(u"Text to Display"),
                                 description=_(u"Display the below text in the portlet.  HTML is OK."),
                                 required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ITopPortlet)

    # TODO: Set default values for the configurable parameters here

    text_field = u'<p>One of the longest running online reefkeeping magazines worldwide, Advanced Aquarist is a hub of for those wanting to advance their reefkeeping skills and learn more about the animals they keep.</p> <p class="hide">What will you find here?  Articles on how to care for saltwater fish and coral, reviews of the latest books, products and equipment, news about what&apos;s happening in the hobby, educational videos, and tips on becoming a better reefkeeper.</p>'

    # TODO: Add keyword parameters for configurable parameters here
    def __init__(self, some_field=u""):
        self.text_field = text_field

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Top Portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('topportlet.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = aq_inner(self.context)
    
    @property
    def text(self):
        """Get the Facebook javascript from the portlet"""
        data = self.data
        text_field = data.text_field
        return text_field 

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ITopPortlet)

    def create(self, data):
        return Assignment(**data)


# NOTE: If this portlet does not have any configurable parameters, you
# can use the next AddForm implementation instead of the previous.

# class AddForm(base.NullAddForm):
#     """Portlet add form.
#     """
#     def create(self):
#         return Assignment()


# NOTE: If this portlet does not have any configurable parameters, you
# can remove the EditForm class definition and delete the editview
# attribute from the <plone:portlet /> registration in configure.zcml


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(ITopPortlet)
