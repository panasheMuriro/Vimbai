// src/components/Avatar.tsx
import React from "react";

interface AvatarProps {
  src: string;   // path inside public folder
  alt?: string;
  size?: number; // size in px
}

const Avatar: React.FC<AvatarProps> = ({ src, alt = "avatar", size = 48 }) => {
  return (
    <img
      src={`${src}`} // ✅ loads from /public
      alt={alt}
      className="rounded-full object-cover border-4 border-black"
      style={{ width: size, height: size, margin: "auto" }}
    />
  );
};

export default Avatar;
