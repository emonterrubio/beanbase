/**
 * Country hero images sourced from Veranda (hips.hearstapps.com CDN).
 * @see https://www.veranda.com/travel/
 */
const HEARST_CDN = "https://hips.hearstapps.com/hmg-prod/images";

/** Veranda image filename per coffee-producing country */
const COUNTRY_IMAGE_FILES: Record<string, string> = {
  Bolivia: "aerial-view-of-amazon-rainforest-in-peru-royalty-free-image-1758638287.pjpeg",
  Brazil: "mata-atlantica-atlantic-forest-in-brazil-royalty-free-image-1719601616.jpg",
  Burundi: "kenya-suyian-lodge-guest-area-exterior-6766f9b60d6ff.jpg",
  Colombia: "guatape-colombia-1594925778.jpg",
  "Costa Rica": "sunset-in-monteverde-royalty-free-image-1728411398.jpg",
  Ecuador: "luxury-cruising-m-y-kontiki-wayri-ship-1666885845.jpg",
  "El Salvador": "sunset-in-monteverde-royalty-free-image-1728411398.jpg",
  Ethiopia: "dallol-danakil-depression-ethiopia-the-hottest-royalty-free-image-1625765852.jpg",
  Guatemala: "sunset-in-monteverde-royalty-free-image-1728411398.jpg",
  Honduras:
    "bamboo-forest-and-entryway-to-lancetilla-arboretum-royalty-free-image-1743389248.pjpeg",
  Indonesia: "pura-ulun-danu-bratan-temple-in-bali-royalty-free-image-1719601267.jpg",
  Kenya: "kenya-suyian-lodge-guest-area-exterior-6766f9b60d6ff.jpg",
  Mexico: "narrow-street-in-the-old-town-of-san-miguel-de-royalty-free-image-1719599371.jpg",
  Nicaragua:
    "bamboo-forest-and-entryway-to-lancetilla-arboretum-royalty-free-image-1743389248.pjpeg",
  Panama: "e78e09d4-0e24-4b32-bf65-a1e68f5f690e.jpg",
  Peru: "majestic-mountain-landscape-machu-picchu-peru-royalty-free-image-1658260333.jpg",
  Rwanda: "kenya-suyian-lodge-guest-area-exterior-6766f9b60d6ff.jpg",
  Tanzania: "kenya-suyian-lodge-guest-area-exterior-6766f9b60d6ff.jpg",
  Uganda: "kenya-suyian-lodge-guest-area-exterior-6766f9b60d6ff.jpg",
  Yemen: "ait-benhaddou-ancient-city-in-morocco-north-africa-royalty-free-image-1719603392.jpg",
};

const DEFAULT_IMAGE =
  "mata-atlantica-atlantic-forest-in-brazil-royalty-free-image-1719601616.jpg";

export function countryImageUrl(country: string | null | undefined, width = 640): string {
  const filename = (country && COUNTRY_IMAGE_FILES[country]) || DEFAULT_IMAGE;
  return `${HEARST_CDN}/${filename}?crop=1xw:1xh;center,top&resize=${width}:*`;
}
