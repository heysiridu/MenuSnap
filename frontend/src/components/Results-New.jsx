import React from "react";
import {
  Image as ImageIcon,
  ArrowLeft,
  ArrowRight,
  Plus,
  Ellipsis,
  Loader2,
  ChevronDown,
  Smile,
  Share,
} from "lucide-react";

const MenuItemCard = ({ item }) => {
  const [imageError, setImageError] = React.useState(false);
  const [imageLoaded, setImageLoaded] = React.useState(false);
  const [useThumbnail, setUseThumbnail] = React.useState(false);
  
  const mainUrl = item.image?.url || item.image?.link || null;
  const thumbnailUrl = item.image?.thumbnailLink || null;
  const currentImageUrl = useThumbnail ? thumbnailUrl : mainUrl;
  const hasAnyImage = mainUrl || thumbnailUrl;
  
  const handleImageError = () => {
    if (!useThumbnail && thumbnailUrl) {
      setUseThumbnail(true);
      setImageLoaded(false);
    } else {
      setImageError(true);
    }
  };
  
  return (
    <div className="flex flex-col">
      <div className="w-full aspect-[4/3] rounded-lg overflow-hidden bg-gray-100 relative">
        {currentImageUrl && !imageError ? (
          <>
            <img
              src={currentImageUrl}
              alt={item.dish}
              className={`w-full h-full object-cover transition-opacity duration-300 ${imageLoaded ? 'opacity-100' : 'opacity-0'}`}
              onLoad={() => setImageLoaded(true)}
              onError={handleImageError}
              referrerPolicy="no-referrer"
            />
            {!imageLoaded && (
              <div className="absolute inset-0 flex items-center justify-center">
                <Loader2 className="w-6 h-6 animate-spin text-black/30" />
              </div>
            )}
          </>
        ) : (
          <div className="w-full h-full flex items-center justify-center text-black/30">
            <ImageIcon className="w-10 h-10" />
          </div>
        )}
      </div>
      <div className="mt-2">
        <h3 className=" text-sm leading-tight">{item.dish}</h3>
        {item.description && (
          <p className="text-xs text-gray-500 mt-0.5 leading-tight">{item.description}</p>
        )}
        {item.price && !item.description && (
          <p className="text-xs text-gray-500 mt-0.5">{item.price}</p>
        )}
      </div>
    </div>
  );
};

export default function Results({ 
  results, 
  previewImage, 
  onScanAnother, 
  onNewScan 
}) {
  if (!results) return null;

  const menuItems = results.menu_with_images || [];
  const appetizers = menuItems.slice(0, 2);
  const mainCourse = menuItems.slice(2);
  
  return (
    <div className="mx-auto max-w-sm bg-[#ffffff] min-h-screen flex flex-col">
      <div className="flex-1 px-4 pt-6 pb-24">
        

        <div className="flex items-center justify-between mb-4 pb-2 border-b-2 border-black/20">
          <div className="flex items-center gap-2">
            <button
              onClick={onScanAnother}
              className="p-1"
              aria-label="Back"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <h1 className="text-lg">New Restaurant</h1>
          </div>
          <div className="flex items-center gap-2">
            <button className="flex items-center gap-1 text-sm px-3 py-0.2 rounded-full border border-black/20 bg-white">
              English
              <ChevronDown className="w-4 h-4" />
            </button>
            <button className="flex items-center gap-1 text-sm px-3 py-0.2 rounded-full border border-black/20 bg-white">
              Save
            </button>
          </div>
        </div>

        {appetizers.length > 0 && (
          <div className="mb-6">
            <h2 className="text-base font-semibold mb-3">Appetizer</h2>
            <div className="grid grid-cols-2 gap-4">
              {appetizers.map((item, index) => (
                <MenuItemCard key={index} item={item} />
              ))}
            </div>
          </div>
        )}

        {mainCourse.length > 0 && (
          <div className="mb-6">
            <h2 className="text-base font-semibold mb-3">Main Course</h2>
            <div className="grid grid-cols-2 gap-4">
              {mainCourse.map((item, index) => (
                <MenuItemCard key={index} item={item} />
              ))}
            </div>
          </div>
        )}

        {menuItems.length === 0 && (
          <div className="text-center text-gray-500 py-10">
            No menu items found
          </div>
        )}
      </div>

      
    </div>
  );
}
