// src/components/BlogCard.tsx
import { SquarePen, Clock, User, MoreHorizontal } from "lucide-react";
import { useState } from "react";

interface BlogCardProps {
  category: string;
  content: string;
  date: string;
  maxChars?: number;
}

export default function BlogCard({
  category,
  content,
  date,
  maxChars = 250,
}: BlogCardProps) {
  const [expanded, setExpanded] = useState(false);

  const isTooLong = content.length > maxChars;
  const displayedText =
    isTooLong && !expanded ? content.substring(0, maxChars) + "..." : content;

  return (
    <div className="relative mb-8 overflow-hidden rounded-[40px] border-2 border-black bg-[#fff3e0] shadow-[8px_8px_0_0_#000]">
      {/* Top Bar */}
      <div className="flex items-center justify-between p-4">
        <div className="flex items-center space-x-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full text-white bg-[#e76f51] shadow-md">
            <SquarePen size={20} />
          </div>
          <div>
            <h3 className="font-bold text-base text-black">{category}</h3>
            <div className="flex items-center text-sm text-gray-700">
              <User size={14} className="mr-1" />
              <span>Vimbai</span>
              <span className="mx-2">•</span>
              <Clock size={14} className="mr-1" />
              <span>{date}</span>
            </div>
          </div>
        </div>
        <button>
          <MoreHorizontal size={24} />
        </button>
      </div>

      {/* Post Content */}
      <div className="p-4 pt-0">
        <p className="text-gray-900 leading-relaxed text-base">
          {displayedText.split("*").map((part, i) =>
            i % 2 === 1 ? (
              <strong key={i} className="font-bold">
                {part}
              </strong>
            ) : (
              part
            )
          )}
        </p>
        {isTooLong && (
          <div className="mt-2">
            <button
              onClick={() => setExpanded(!expanded)}
              className="text-blue-600 hover:text-blue-800"
            >
              {expanded ? "Show Less" : "See More"}
            </button>
          </div>
        )}
      </div>

      {/* Action Bar */}
      <div className="relative flex justify-between p-4 border-t-2 border-black bg-[#e76f51]">
        {/* Placeholder for actions */}
      </div>
    </div>
  );
}
