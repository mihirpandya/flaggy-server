What works:

o Under the default policy, email6 should be completely backward
  compatible with email5.1 (the version of email in Python 3.2).

o all headers are objects now.  The 'source' attribute gives access
  to whatever the parser read from the source (possibly including
  surrogateescaped bytes), while the 'value' attribute gives access to the
  decoded version of the header.

o date headers can be set to a datetime (see utils.localtime for
  how to set a date header to the current local time).

o date headers have a 'datetime' attribute

o address headers have 'groups' and 'addresses' attributes.
    A Group is a list of Address objects, as is addresses, but
    the latter is *all* the addresses in the header, including
    those inside groups (if any).

o Group has the following attributes:

    name
    addresses

  if name is None, addresses is a list of a single Address object and
  represents a non-Group that occurred in the address header.

o Address objects have the following attributes:

    name
    username
    domain
    addr_spec

o if you use policy=email6_defaults the header values will be
  the decoded values of the header (ie: unicode characters
  instead of encoded words).

o You may assign strings containing non-ASCII characters to
  headers, and for unstructured headers they will be encoded
  correctly when the message is flattened.

o Header now defaults to encoding using utf-8 if no charset is
  specified and the string contains non-ASCII characters.

o You can play around with customizing the header_factory.


What doesn't work yet:

o if you set a structured header to a string containing
  non-ASCII, it will *not* be flattened properly

o encoded words in address headers are not yet decoded.

o Only date and address headers currently have extra attributes,
  for all other structured headers you still need to use
  the Message methods to set and query parameters.

o The parser still builds the model using only normal Message
  objects (that is, while the header_factory has been implemented
  the message_factory hasn't been).

o You can't use email6 Message objects with the Mailbox module
  due to a cross-module dependency in that module.  (You can
  use them with smtplib, though).

o There is currently no way to control the 'unique header'
  enforcement other than customizing the classes in the
  header_factory.

o Many other things I'm not thinking about at the moment :)
