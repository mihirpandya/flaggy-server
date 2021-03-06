# Copyright (C) 2001-2006 Python Software Foundation
# Author: Barry Warsaw
# Contact: email-sig@python.org

"""email package exception classes."""



class MessageError(Exception):
    """Base class for errors in the email package."""


class MessageParseError(MessageError):
    """Base class for message parsing errors."""


class HeaderParseError(MessageParseError):
    """Error while parsing headers."""


class BoundaryError(MessageParseError):
    """Couldn't find terminating boundary."""


class MultipartConversionError(MessageError, TypeError):
    """Conversion to a multipart is prohibited."""


class CharsetError(MessageError):
    """An illegal charset was given."""



# These are parsing defects which the parser was able to work around.
class MessageDefect(Exception):
    """Base class for a message defect."""

    def __init__(self, line=None):
        self.line = line

class NoBoundaryInMultipartDefect(MessageDefect):
    """A message claimed to be a multipart but had no boundary parameter."""

class StartBoundaryNotFoundDefect(MessageDefect):
    """The claimed start boundary was never found."""

class FirstHeaderLineIsContinuationDefect(MessageDefect):
    """A message had a continuation line as its first header line."""

class MisplacedEnvelopeHeaderDefect(MessageDefect):
    """A 'Unix-from' header was found in the middle of a header block."""

class MalformedHeaderDefect(MessageDefect):
    """Found a header that was missing a colon, or was otherwise malformed."""

class MultipartInvariantViolationDefect(MessageDefect):
    """A message claimed to be a multipart but no subparts were found."""

class InvalidMultipartContentTransferEncodingDefect(MessageDefect):
    """An invalid content transfer encoding was set on the multipart itself."""

class DuplicateHeaderDefect(MessageDefect):
    """Multiple instances of a required-to-be-unique header were found"""

    def __init__(self, header_name):
        super().__init__(header_name)
        self.header_name = header_name.lower()

    def __str__(self):
        return ("there may only be one '{}' header per "
                "message").format(self.arg[0])

# These errors are specific to header parsing.

class HeaderDefect(Exception):
    """Base class for a header defect."""

class InvalidHeaderDefect(HeaderDefect):
    """Header is not valid, message gives details."""

class HeaderMissingRequiredValue(HeaderDefect):
    """A header that must have a value had none"""

class NonPrintableDefect(HeaderDefect):
    """ASCII characters outside the ascii-printable range found"""

    def __init__(self, non_printables):
        super().__init__(non_printables)
        self.non_printables = non_printables

    def __str__(self):
        return ("the following ASCII non-printables found in header: "
            "{}".format(self.non_printables))

class ObsoleteHeaderDefect(HeaderDefect):
    """Header uses syntax declared obsolete by RFC 5322"""

class UndecodableBytesDefect(HeaderDefect):
    """Header contained bytes that could not be decoded"""

class InvalidBase64PaddingDefect(HeaderDefect):
    """base64 encoded sequence had an incorrect length"""

class InvalidBase64CharactersDefect(HeaderDefect):
    """base64 encoded sequence had characters not in base64 alphabet"""
