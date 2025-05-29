#Copyright @ISmartDevs
#Channel t.me/TheSmartDev

from .dlxutils.fb import setup_fb_handlers
from .dlxutils.insta import setup_insta_handlers
from .dlxutils.pin import setup_pinterest_handler
from .dlxutils.spfy import setup_spotify_handler
from .dlxutils.tik import setup_tt_handler
from .dlxutils.yt import setup_yt_handler
from .hlpxutils.help import setup_help_handler
from .infoxutils.info import setup_info_handler
from .netxutils.ip import setup_ip_handlers
from .netxutils.px import setup_px_handler
from .privxutils.privacy import setup_privacy_handler
from .webxutils.ss import setup_ss_handler

def setup_modules_handlers(app):
    setup_fb_handlers(app)
    setup_insta_handlers(app)
    setup_pinterest_handler(app)
    setup_spotify_handler(app)
    setup_tt_handler(app)
    setup_yt_handler(app)
    setup_help_handler(app)
    setup_info_handler(app)
    setup_ip_handlers(app)
    setup_px_handler(app)
    setup_privacy_handler(app)
    setup_ss_handler(app)