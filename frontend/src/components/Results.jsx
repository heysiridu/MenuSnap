import React, { useState } from "react";
import {
  Image as ImageIcon,
  ArrowLeft,
  Plus,
  Ellipsis,
  Loader2,
  X,
  Globe, // 新增：图标
} from "lucide-react";

const MenuItemCard = ({ item, currentLang }) => {
  const [imageError, setImageError] = React.useState(false);
  const [imageLoaded, setImageLoaded] = React.useState(false);
  const [useThumbnail, setUseThumbnail] = React.useState(false);

  // --- 逻辑：读取对应语言的菜名 ---
  // 如果后端返回了 translations，读取对应语言，否则回退到原始 dish 名称
  const displayName = item.translations?.[currentLang] || item.dish;
  
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
    <div className="flex gap-4 p-3 bg-white rounded-xl border border-black/10 shadow-sm">
      <div className="w-20 h-20 flex-shrink-0 rounded-lg overflow-hidden bg-black/5 relative">
        {currentImageUrl && !imageError ? (
          <>
            <img
              src={currentImageUrl}
              alt={displayName}
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
            <ImageIcon className="w-8 h-8" />
          </div>
        )}
      </div>
      <div className="flex-1 min-w-0">
        <h3 className="font-semibold text-sm truncate">{displayName}</h3>
        {item.price && (
          <p className="text-xs text-black/60 mt-1">{item.price}</p>
        )}
        {hasAnyImage && !imageError && (
          <a
            href={mainUrl || thumbnailUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-blue-600 hover:underline mt-2 inline-block"
          >
            {currentLang === 'zh' ? '查看原图' : currentLang === 'es' ? 'Ver imagen' : 'View full image'}
          </a>
        )}
      </div>
    </div>
  );
};

const PillButton = ({ children, onClick, className = "" }) => (
  <button
    onClick={onClick}
    className={`inline-flex items-center justify-center
                h-11 px-5 rounded-2xl border border-black/100 bg-white
                text-sm font-medium shadow-sm whitespace-nowrap
                active:scale-[0.99] text-xs ${className}`}
  >
    {children}
  </button>
);

export default function Results({ 
  results, 
  previewImage, 
  onScanAnother, 
  onNewScan 
}) {
  // --- 状态：当前语言 (zh: 中文, en: 英文, es: 西班牙语) ---
  const [currentLang, setCurrentLang] = useState("zh");

  if (!results) return null;

  // 简单的 UI 文本翻译映射
  const uiTexts = {
    zh: { title: "菜单识别结果", found: "识别到", items: "项菜品", button: "扫描下一张", time: "识别耗时" },
    en: { title: "Menu Results", found: "Found", items: "Menu Items", button: "Scan Another Menu", time: "OCR processing time" },
    es: { title: "Resultados del Menú", found: "Encontrado", items: "Artículos", button: "Escanear otro", time: "Tiempo OCR" }
  };

  const t = uiTexts[currentLang];
  
  return (
    <div className="mx-auto max-w-sm px-4 pb-4 pt-1 text-black min-h-screen">
      {/* --- 修改：顶部导航栏添加下拉菜单 --- */}
      <div className="sticky top-0 z-10 -mx-4 mb-3 flex items-center justify-between bg-white/80 backdrop-blur-sm px-4 pt-3 pb-2 border-b border-black/5">
        <button
          aria-label="Back"
          onClick={onScanAnother}
          className="rounded-full p-2 hover:bg-black/[0.06]"
        >
          <ArrowLeft className="h-5 w-5" />
        </button>
        
        <h2 className="text-sm font-semibold truncate px-2">{t.title}</h2>

        <div className="relative flex items-center gap-1 bg-black/5 rounded-full px-2 py-1">
          <Globe className="w-3 h-3 text-black/50" />
          <select 
            value={currentLang}
            onChange={(e) => setCurrentLang(e.target.value)}
            className="bg-transparent text-[10px] font-bold focus:outline-none appearance-none pr-1"
          >
            <option value="zh">中文</option>
            <option value="en">EN</option>
            <option value="es">ES</option>
          </select>
        </div>
      </div>

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">
            {t.found} {results.dishes_found} {t.items}
          </h2>
        </div>
        
        {previewImage && (
          <div className="rounded-xl overflow-hidden border border-black/10">
            <img
              src={previewImage}
              alt="Uploaded menu"
              className="w-full h-40 object-cover"
            />
          </div>
        )}

        <p className="text-xs text-black/60">
          {t.time}: {results.ocr_time?.toFixed(2)}s
        </p>

        <div className="space-y-3">
          {results.menu_with_images?.map((item, index) => (
            <MenuItemCard key={index} item={item} currentLang={currentLang} />
          ))}
        </div>

        <PillButton onClick={onScanAnother} className="w-full mt-4">
          {t.button}
        </PillButton>
      </div>

      <div className="sticky bottom-3 mt-6 flex w-full items-center justify-between gap-3">
        <button onClick={onScanAnother} className="rounded-full p-3 shadow-sm border border-black/10 bg-white">
          <ArrowLeft className="h-5 w-5" />
        </button>
        <button onClick={onNewScan} className="grid h-12 w-12 place-items-center rounded-full bg-black text-white shadow">
          <Plus className="h-6 w-6" />
        </button>
        <button className="rounded-full p-3 shadow-sm border border-black/10 bg-white">
          <Ellipsis className="h-5 w-5" />
        </button>
      </div>
    </div>
  );
}