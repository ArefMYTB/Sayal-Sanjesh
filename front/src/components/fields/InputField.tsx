// Custom components
function InputField(props: {
  id: string;
  label?: string;
  extra?: string;
  placeholder: string;
  variant?: string;
  state?: string | number;
  setState?: React.Dispatch<any>;
  defaultValue?: null | string | number;
  border?: "err" | "success" | "dis" | "normal";
  disabled?: boolean;
  type?: "text" | "text-aria" | "password" | "number" | "email" | "tel";
}) {
  const {
    label,
    id,
    extra,
    type,
    defaultValue,
    placeholder,
    variant,
    state,
    disabled,
    setState,
    border,
  } = props;

  return (
    <div className={`${extra}`}>
      {label ? (
        <label
          htmlFor={id}
          className={`text-sm text-navy-700 dark:text-white ${
            variant === "auth" ? "ml-1.5 font-medium" : "ml-3 font-bold"
          }`}
        >
          {label}
        </label>
      ) : (
        <></>
      )}
      {type === "text-aria" ? (
        <textarea
          disabled={disabled}
          rows={3}
          id={id}
          placeholder={placeholder}
          value={state}
          onChange={(e) => (setState ? setState(e.target.value) : null)}
          className={`mt-2 flex h-12 min-h-[150px] w-full items-center justify-center rounded-xl border bg-white/0 p-3 text-sm outline-none ${
            border === "dis"
              ? "!border-none !bg-gray-100 dark:!bg-white/5 dark:placeholder:!text-[rgba(255,255,255,0.15)]"
              : border === "err"
              ? "border-red-500 text-red-500 placeholder:text-red-500 dark:!border-red-400 dark:!text-red-400 dark:placeholder:!text-red-400"
              : border === "success"
              ? "border-green-500 text-green-500 placeholder:text-green-500 dark:!border-green-400 dark:!text-green-400 dark:placeholder:!text-green-400"
              : "border-gray-200 dark:!border-white/10 dark:text-white"
          }`}
        />
      ) : (
        <input
          disabled={disabled}
          type={type}
          id={id}
          defaultValue={defaultValue}
          value={state}
          onChange={(e) => (setState ? setState(e.target.value) : null)}
          placeholder={placeholder}
          className={`mt-2 flex h-12 w-full items-center justify-center rounded-xl border bg-white/0 p-3 text-sm outline-none ${
            border === "dis"
              ? "!border-none !bg-gray-100 dark:!bg-white/5 dark:placeholder:!text-[rgba(255,255,255,0.15)]"
              : border === "err"
              ? "border-red-500 text-red-500 placeholder:text-red-500 dark:!border-red-400 dark:!text-red-400 dark:placeholder:!text-red-400"
              : border === "success"
              ? "border-green-500 text-green-500 placeholder:text-green-500 dark:!border-green-400 dark:!text-green-400 dark:placeholder:!text-green-400"
              : "border-gray-200 dark:!border-white/10 dark:text-white"
          }`}
        />
      )}
    </div>
  );
}

export default InputField;
