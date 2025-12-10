import React from "react";
import {
  Camera,
  Image as ImageIcon,
  ChevronRight,
  ArrowLeft,
  Plus,
  Ellipsis,
} from "lucide-react";

const SectionCard = ({ children, className = "" }) => (
  <div
    className={`rounded-2xl border border-black/100 bg-white p-5 shadow-sm ${className}`}
  >
    {children}
  </div>
);

const ActionButton = ({ icon, title, subtitle, onClick }) => (
  <button
    onClick={onClick}
    className="w-full rounded-xl border border-black/100 bg-white p-4 text-left transition active:scale-[0.99]"
  >
    <div className="flex items-center gap-3">
      <div className="grid h-12 w-12 place-items-center rounded-xl bg-black/[0.04]">
        {icon}
      </div>
      <div>
        <div className="text-sm font-semibold">{title}</div>
        <div className="text-xs text-black/60">{subtitle}</div>
      </div>
    </div>
  </button>
);

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

const RecentMenuCard = ({ item, onOpen }) => (
  <button
    onClick={() => onOpen?.(item.id)}
    className="min-w-[220px] max-w-[220px] overflow-hidden rounded-xl border border-black/10 bg-white text-left shadow-sm"
  >
    <div className="h-32 w-full overflow-hidden">
      <img
        src={item.imageUrl}
        alt={item.title}
        className="h-full w-full object-cover"
      />
    </div>
    <div className="p-3">
      <div className="text-sm font-semibold leading-tight">{item.title}</div>
      <div className="mt-1 text-xs text-black/60">{item.date}</div>
    </div>
  </button>
);

export default function MenuSnapHome({
  recent = [
    {
      id: "jinramen",
      title: "Jin Ramen",
      date: "Oct 23rd 2025 7:35 PM",
      imageUrl:
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHv0xhJT-XnLaVvAoKXbo2gddLN4mfD4Qf4w&s",
    },
    {
      id: "heytea",
      title: "Hey Tea",
      date: "Oct 22nd 2025 6:35 PM",
      imageUrl:
        "https://downtownbrooklyn.com/wp-content/uploads/2024/09/Heytea.jpg",
    },
  ],
  onPickFromGallery,
  onOpenCamera,
  onOpenDemo,
  onOpenSettings = () => console.log("settings"),
  onOpenRecent = (id) => console.log("open recent", id),
  onBack = () => console.log("back"),
  onMore = () => console.log("more"),
  error,
}) {
  return (
    <div className="mx-auto max-w-sm px-4 pb-4 pt-1 text-black">
      <div className="sticky top-0 z-10 -mx-4 mb-3 flex items-center justify-between bg-transparent px-4 pt-3">
        <button
          aria-label="Back"
          onClick={onBack}
          className="rounded-full p-2 hover:bg-black/[0.06]"
        >
          <ArrowLeft className="h-5 w-5" />
        </button>
        <button
          aria-label="More"
          onClick={onMore}
          className="rounded-full p-2 hover:bg-black/[0.06]"
        >
          <Ellipsis className="h-5 w-5" />
        </button>
      </div>

      <SectionCard className="mt-2">
        <div className="mx-auto mb-3 grid h-24 w-24 place-items-center rounded-full bg-black/[0.06]">
          <Camera className="h-10 w-10 text-black/70" />
        </div>
        <div className="text-center">
          <h1 className="text-xl">Take a Picture of Your Menu</h1>
          <p className="mx-auto mt-2 max-w-xs text-xs text-black/70">
            Snap a photo or pick one from your gallery to begin! You'll get
            clear photos and translations for every item on the menu.
          </p>
        </div>

        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-xl">
            <p className="text-sm text-red-600 text-center">{error}</p>
          </div>
        )}

        <div className="mt-5 grid grid-cols-10 gap-3">
          <div className="col-span-5">
            <ActionButton
              icon={<ImageIcon />}
              title="Gallery"
              subtitle="Choose from photos"
              onClick={onPickFromGallery}
            />
          </div>
          <div className="col-span-5">
            <ActionButton
              icon={<Camera />}
              title="Camera"
              subtitle="Take a Photo"
              onClick={onOpenCamera}
            />
          </div>
        </div>
      </SectionCard>

      <div className="mt-4 grid grid-cols-2 gap-2">
        <PillButton onClick={onOpenSettings} className="w-full">
          Settings
        </PillButton>
        <PillButton onClick={onOpenDemo} className="w-full">
          Try Demo Menu
        </PillButton>
      </div>

      <div className="mt-6 flex items-center justify-between">
        <h2 className="text-lg font-semibold">Your Recent Menus</h2>
        <button
          className="rounded-full p-1 hover:bg-black/[0.06]"
          aria-label="See all"
        >
          <ChevronRight className="h-5 w-5" />
        </button>
      </div>

      <div className="mt-3 flex gap-4 overflow-x-auto pb-1">
        {recent.map((r) => (
          <RecentMenuCard key={r.id} item={r} onOpen={onOpenRecent} />
        ))}
      </div>

      <div className="sticky bottom-3 mt-6 flex w-full items-center justify-between gap-3">
        <button
          onClick={onBack}
          className="rounded-full p-3 shadow-sm border border-black/10 bg-white"
        >
          <ArrowLeft className="h-5 w-5" />
        </button>
        <button
          onClick={onPickFromGallery}
          className="grid h-12 w-12 place-items-center rounded-full bg-black text-white shadow"
        >
          <Plus className="h-6 w-6" />
        </button>
        <button
          onClick={onMore}
          className="rounded-full p-3 shadow-sm border border-black/10 bg-white"
        >
          <Ellipsis className="h-5 w-5" />
        </button>
      </div>
    </div>
  );
}
