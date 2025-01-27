import DatePicker from "react-datepicker2";
interface DateInputProps {
  label: string;
  value: any;
  onChange: Function;
}
const DateInput = (props: DateInputProps) => {
  const { label, value, onChange } = props;
  return (
    <div className="">
      <label
        // htmlFor={id}
        className={`ml-3 text-sm font-bold text-navy-700 dark:text-white`}
      >
        {label}
      </label>
      <DatePicker
        isGregorian={false}
        timePicker={false}
        value={value}
        onChange={(value) => onChange(value)}
      />
    </div>
  );
};
export default DateInput;
