# Import all models here so SQLAlchemy mapper can resolve relationships at startup
from app.models.origin import Origin  # noqa: F401
from app.models.farm import Farm  # noqa: F401
from app.models.auction_event import AuctionEvent  # noqa: F401
from app.models.lot import Lot  # noqa: F401
from app.models.certification import Certification  # noqa: F401
