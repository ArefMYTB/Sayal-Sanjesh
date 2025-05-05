import { useState } from "react";
import FileUploader from "components/fields/ImageUpload";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";
import moment from "moment-jalaali";
import DatePicker from "react-datepicker2";

moment.loadPersian({ dialect: "persian-modern", usePersianDigits: false });

interface SnapshotFormProps {
  onClose: Function;
  serialnumber: string;
  refetchSnapshots: () => void;
}

const SnapshotForm = (props: SnapshotFormProps) => {
  const { onClose, serialnumber, refetchSnapshots } = props;
  const [watermeterId, setWatermeterId] = useState(serialnumber);
  const [createDate, setCreateDate] = useState(() => moment().locale("fa")); // mm/dd/yy
  const [createTime, setCreateTime] = useState(() => moment().format("HH:mm")); // hh/MM/ss
  const [mechanicValue, setMechanicValue] = useState("");
  const [cumulativeValue, setCumulativeValue] = useState("");
  const [text, setText] = useState("");
  const [imageUrl, setImageUrl] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!watermeterId) {
      renderToast("اطلاعات الزامی وارد نشده است", "warn");
      return;
    }

    // Convert Jalali date + time to Gregorian
    // Extract time from the input
    const [hour, minute] = createTime.split(":").map(Number);

    // Step 1: Set the time on the Jalali moment
    const jalaliWithTime = createDate.clone().set({
      hour,
      minute,
      second: 0,
      millisecond: 0,
    });
    // Step 2: Convert to Gregorian properly
    const gregorian = moment(
      jalaliWithTime.format("jYYYY/jMM/jDD HH:mm"),
      "jYYYY/jMM/jDD HH:mm"
    );
    // Final values to send to Django
    const create_date = gregorian.format("YYYY-MM-DD"); // e.g., "2025-05-05"
    const create_time = gregorian.format("HH:mm");

    const payload = {
      watermeter_id: watermeterId,
      create_date: create_date,
      create_time: create_time,
      mechanic_value: parseFloat(mechanicValue),
      cumulative_value: parseFloat(cumulativeValue),
      text,
      image: [imageUrl], // Expecting array in backend
    };

    const response = await reqFunction("snapshots/admin/create", payload);

    if (response.code === 200) {
      renderToast("ثبت با موفقیت انجام شد", "success");
      // Optionally reset the form
      setWatermeterId("");
      // setCreateDate("");
      setCreateTime("");
      setMechanicValue("");
      setCumulativeValue("");
      setText("");
      setImageUrl(null);
      // Close form and refresh table
      onClose();
      refetchSnapshots();
    } else {
      renderToast(response.farsi_message || "خطا در ثبت", "err");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block">شماره سریال کنتور</label>
        <input
          type="text"
          value={watermeterId}
          onChange={(e) => setWatermeterId(e.target.value)}
          className="w-full rounded border p-2"
        />
      </div>

      <div>
        <label className="block">مقدار مکانیکی</label>
        <input
          type="number"
          value={mechanicValue}
          onChange={(e) => setMechanicValue(e.target.value)}
          className="w-full rounded border p-2"
        />
      </div>

      <div>
        <label className="block">تاریخ ایجاد</label>
        <DatePicker
          isGregorian={false}
          value={createDate}
          onChange={(value) => setCreateDate(value)}
          timePicker={false}
          inputFormat="jYYYY/jMM/jDD"
        />
      </div>

      <div>
        <label className="block">زمان ایجاد</label>
        <input
          type="time"
          value={createTime}
          onChange={(e) => setCreateTime(e.target.value)}
          className="w-full rounded border p-2"
        />
      </div>

      <div>
        <label className="block">مقدار تجمعی</label>
        <input
          type="number"
          value={cumulativeValue}
          onChange={(e) => setCumulativeValue(e.target.value)}
          className="w-full rounded border p-2"
        />
      </div>

      <div>
        <label className="block">توضیحات</label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="w-full rounded border p-2"
        ></textarea>
      </div>

      <div>
        <label className="block">تصویر</label>
        <FileUploader
          preview={imageUrl}
          setPreview={setImageUrl}
          uploaderType="projectImage"
          uploadEndpoint="snapshots/admin/upload"
        />
      </div>

      <button
        type="submit"
        className="w-full rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
      >
        ثبت برداشت
      </button>
    </form>
  );
};

export default SnapshotForm;
