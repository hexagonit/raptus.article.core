User story
==========

A scripted walk-through of basic features of Raptus Article.

Adding an Article
-----------------

We'll start by adding a Raptus Article. It's a normal content-type
which we can add with the `Add new ...` drop-down menu.

To use this menu, we first need to login.

    Go to login screen.
    >>> browser.open(portal.absolute_url() + '/login')

    Fill in your credentials.
    >>> browser.getControl(name='__ac_name').value = TEST_USER_NAME
    >>> browser.getControl(name='__ac_password').value = TEST_USER_PASSWORD

    Click Login button.
    >>> browser.getControl(name='submit').click()

    Are we logged in?
    >>> "You are now logged in" in browser.contents
    True


Since we are now logged-in let's locate the `Add new ...` drop-down menu and
start adding a new Article.

    Verify that we have the link to create an Article.
    >>> browser.open(portal.absolute_url() + '/')
    >>> browser.getLink(id='article').url.endswith("createObject?type_name=Article")
    True

    Click on the add link to open the form for adding an Article.
    >>> browser.getLink(id='article').click()

    Fill in fields.
    >>> browser.getControl(name='title').value = "Ñinjas Ättack"
    >>> browser.getControl(name='description').value = "Ättack of the Ñinjas. People ängry."
    >>> browser.getControl(name='text').value = "<b>Who doësn't like ättacking ninjas?</b>"

    Click submit to create the article.
    >>> browser.getControl(name='form.button.save').click()

    Was our article really created?
    >>> 'ninjas-attack' in portal.objectIds()
    True

    Are articles fields visible?
    >>> "Ñinjas Ättack" in browser.contents
    True
    >>> "Ättack of the Ñinjas. People ängry." in browser.contents
    True
    >>> "<b>Who doësn't like ättacking ninjas?</b>" in browser.contents
    True


Using Components tab
--------------------

Great! Our Article has been successfully created. Now let's see if we can use the
Components tab.

    Verify that we have the link to access Components tab.
    >>> browser.open(portal.absolute_url() + '/ninjas-attack')
    >>> browser.getLink('Components').url.endswith("@@components")
    True

    Click this link to open the form for managing Article's Components.
    >>> browser.getLink('Components').click()

    Out-of-the-box we only have one component avaiable: raptus.article.related. Let's
    check that we have it on the list of available Components.
    >>> 'Related content' in browser.contents
    True
    >>> '++resource++related.gif' in browser.contents
    True
    >>> 'List of related content of the article.' in browser.contents
    True

Now, let's activate a Component by checking it's checkbox and clicking the Save
button.

    Verify that we have a checkbox for 'related' Component and that it's not checked
    >>> browser.getControl('related').selected
    False

    Click on the checkbox to make it selected
    >>> browser.getControl('related').click()

    Save our changes by clicking the Save button.
    >>> browser.getControl(name='form.submitted').click()

    Did we get the success notification?
    >>> 'Components saved successfully' in browser.contents
    True

    The 'related' checkbox should now be selected.
    >>> browser.getControl('related').selected
    True

To get back to where we were, we are now going to use the Components tab to disable
the `related` Component.

    Click on the checkbox to de-select it
    >>> browser.getControl('related').click()

    Save our changes by clicking the Save button.
    >>> browser.getControl(name='form.submitted').click()

    Did we get the success notification?
    >>> 'Components saved successfully' in browser.contents
    True

    The `related` checkbox should now be selected.
    >>> browser.getControl('related').selected
    False


Using the `Save and View` button
--------------------------------

Components tab has an additional button - Save and View. This one allows you to
save your settings and go directly back to the main view of your Article.

    Click the Components tab.
    >>> browser.getLink('Components').click()

    Select a checkbox.
    >>> browser.getControl('related').selected = True

    Click `Save and View` to save your settings and go back to the main view.
    >>> browser.getControl(name='form.view').click()

    Did we get the success notification?
    >>> 'Components saved successfully' in browser.contents
    True

    Are we on the main view of the Article?
    >>> browser.url.endswith('/ninjas-attack')
    True

    Go back to Components tab and check that `related` checkbox is selected.
    >>> browser.getLink('Components').click()
    >>> browser.getControl('related').selected
    True


