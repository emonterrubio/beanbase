"use client";

type Billing = "monthly" | "yearly";

interface Props {
  value: Billing;
  onChange: (v: Billing) => void;
}

export function BillingToggle({ value, onChange }: Props) {
  return (
    <div className="relative inline-flex rounded-full bg-fog-100 p-1">
      {/* Sliding white pill */}
      <div
        aria-hidden
        className={`absolute top-1 bottom-1 w-[calc(50%-4px)] rounded-full bg-white shadow-sm transition-transform duration-300 ease-in-out ${
          value === "yearly" ? "translate-x-[calc(100%+8px)]" : "translate-x-0"
        }`}
        style={{ left: 4 }}
      />

      {(["monthly", "yearly"] as const).map((option) => (
        <button
          key={option}
          onClick={() => onChange(option)}
          className={`relative z-10 w-28 rounded-full py-2 text-sm font-medium capitalize transition-colors duration-200 ${
            value === option ? "text-text" : "text-muted"
          }`}
        >
          {option === "monthly" ? "Monthly" : "Yearly"}
        </button>
      ))}
    </div>
  );
}
