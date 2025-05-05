import { ChangeEvent, useState } from "react";
import NoImage from "../../assets/img/avatars/no-image-icon.png";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";

interface FileUploaderProps {
  preview: string | null;
  setPreview: React.Dispatch<string | null>;
  uploaderType: "projectImage" | "profilePicture";
  uploadEndpoint: string;
}
const FileUploader = (props: FileUploaderProps) => {
  const { preview, setPreview, uploaderType, uploadEndpoint } = props;
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  // const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleFileInputChange = async (
    event: ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (file && file.size <= 512000) {
      setSelectedFile(file);
      if (uploaderType === "profilePicture") {
        const reader = new FileReader();
        reader.onload = () => {
          if (typeof reader.result === "string") {
            // console.log(typeof reader.result);
            setPreview(reader.result);
          }
        };
        reader.readAsDataURL(file);
      } else {
        let data = new FormData();
        data.append("file", file);
        const response = await reqFunction(uploadEndpoint, data);
        // console.log(response);
        if (response.code === 200) {
          // console.log(response.data.fileurl);
          setPreview(response.data.fileurl);
        } else {
          renderToast(
            response?.farsi_message
              ? response.farsi_message
              : "در بارگزاری تصویر خطایی رخ داده",
            "err"
          );
          console.log(selectedFile);
        }
      }
    } else {
      renderToast("حداکثر حجم فایل مجاز 500 کیلوبایت است", "warn");
    }
  };

  return (
    <div className="flex flex-row items-center justify-around">
      <div className="mt-4 h-24 w-24 overflow-hidden rounded-full">
        <img
          src={
            preview
              ? uploaderType === "projectImage"
                ? process.env.REACT_APP_SAYAL_API_ENDPOINT_MAIN + preview
                : preview
              : NoImage
          }
          alt="Selected"
          className=" h-full w-full object-cover"
        />
      </div>

      <label
        htmlFor="file-upload"
        className="cursor-pointer rounded-md bg-blue-500 px-4 py-2 text-white"
      >
        انتخاب تصویر
      </label>
      <input
        type="file"
        id="file-upload"
        accept=".jpg, .jpeg, .png"
        className="hidden"
        onChange={handleFileInputChange}
      />
    </div>
  );
};

export default FileUploader;
