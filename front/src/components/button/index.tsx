interface CustomBtnProps {
  onClick: any;
  text?: string | null;
  icon?: JSX.Element | null;
  color?:
    | "red"
    | "brand"
    | "blue"
    | "green"
    | "yellow"
    | "orange"
    | "navy"
    | "purple"
    | "gray";
  [x: string]: any;
  extra?: string;
  isDisabled?: boolean;
}

const CustomButton = (props: CustomBtnProps) => {
  const { onClick, icon, color, text, extra, isDisabled } = props;
  return (
    <button
      disabled={isDisabled ?? false}
      onClick={onClick}
      className={`ml-4 flex items-center rounded-xl bg-${color}-500 px-3 py-2 text-base font-medium text-white transition duration-200 hover:bg-${color}-600 active:bg-${color}-700 dark:bg-${color}-400 dark:text-white dark:hover:bg-${color}-300 dark:active:bg-${color}-200 ${extra} `}
    >
      {text}
      <span className={`${text ?? ""} text-lg`}>{icon}</span>
    </button>
  );
};
export default CustomButton;
