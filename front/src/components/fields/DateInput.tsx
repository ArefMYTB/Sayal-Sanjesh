import DatePicker from "react-datepicker2";
interface DateInputProps {
  label: string;
  value: any;
  onChange: Function;
  disabled?: boolean;
}
const DateInput = (props: DateInputProps) => {
  const { label, value, onChange, disabled = false } = props;
  return (
    <div className="">
      <label
        // htmlFor={id}
        className={`ml-3 text-sm font-bold text-navy-700 dark:text-white`}
      >
        {label}
      </label>
      <div
        className={`${disabled ? "pointer-events-none opacity-50" : ""}`}
      >
        <DatePicker
          isGregorian={false}
          timePicker={false}
          value={value}
          onChange={(value) => onChange(value)}
        />
      </div>
    </div>
  );
};
export default DateInput;
