"use client";

type Billing = "monthly" | "yearly";

interface Props {
  value: Billing;
  onChange: (v: Billing) => void;
}

export function BillingToggle({ value, onChange }: Props) {
  return (
    <div className="relative inline-flex rounded-full border border-honey-300 bg-honey-100/30 p-1.5">
      <div
        aria-hidden
        className={`absolute top-1.5 bottom-1.5 w-[calc(50%-8px)] rounded-full bg-white transition-[left] duration-300 ease-in-out ${
          value === "yearly" ? "left-[calc(50%+3px)]" : "left-1.5"
        }`}
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
