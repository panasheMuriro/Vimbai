// src/components/Bio.tsx
import React from "react";
import Avatar from "./Avatar";

interface BioProps {
  name?: string;
  role?: string;
  description?: string;
  avatarSrc?: string;
}

const Bio: React.FC<BioProps> = ({
//   name = "VIMBAI",
  role = "Zimbabwean AI News Reviewer",
  description = "Covering the latest local news, from politics to culture, in a fun casual style 📰✨",
  avatarSrc = "potrait.png", // place your image in public/
}) => {
  return (
    <div className="flex flex-col items-center space-x-4 p-10 text-center max-w-md mx-auto">
      <Avatar src={avatarSrc} size={200} />
      <div>
        <h2 className="font-bold text-lg text-black">VIMB<span className="text-orange-800">AI</span></h2>
        <p className="text-sm text-gray-700 italic">{role}</p>
        <p className="mt-1 text-gray-800 text-sm">{description}</p>
      </div>
    </div>
  );
};

export default Bio;
