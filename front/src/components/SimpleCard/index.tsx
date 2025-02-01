// SimpleCard.tsx
import React, { ReactNode } from "react";

interface SimpleCardProps {
  title: string;
  children: ReactNode;
  extraStyle?: string;
}

const SimpleCard: React.FC<SimpleCardProps> = ({
  title,
  children,
  extraStyle = "",
}) => {
  return (
    <div
      className={`mx-auto max-w-md rounded-lg border p-1 shadow-md ${extraStyle}`}
    >
      {/* Header */}
      <div className="rounded-t-lg bg-gray-200 py-2 text-center font-bold">
        {title}
      </div>

      {/* Content */}
      <div className="space-y-3 p-4 text-right">{children}</div>
    </div>
  );
};

export default SimpleCard;
