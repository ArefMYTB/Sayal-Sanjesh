import Card from "components/card";
import { useNavigate } from "react-router-dom";

const Widget = (props: {
  icon?: null | JSX.Element;
  title: string;
  subtitle: string;
  link?: null | string;
}) => {
  const { icon, title, subtitle, link } = props;
  const navigate = useNavigate();
  return (
    <Card
      onClick={() => (link ? navigate(link) : null)}
      extra={`!flex-row flex-grow items-center rounded-[20px] ${
        link ? "!cursor-pointer" : ""
      } !h-max`}
    >
      {icon ? (
        <div className="mx-4 flex h-[90px] w-auto flex-row  items-center">
          <div className="rounded-full bg-lightPrimary p-3 dark:bg-navy-700">
            <span className="flex items-center text-brand-500 dark:text-white">
              {icon}
            </span>
          </div>
        </div>
      ) : null}

      <div
        className={`h-50 ${
          icon ? "me-4" : "px-2 py-3"
        } flex w-auto flex-col justify-center`}
      >
        <p className="text-md font-dm font-medium text-gray-600 dark:text-white dark:opacity-80">
          {title}
        </p>
        <h4 className=" text-lg font-bold text-navy-700 dark:text-white">
          {subtitle}
        </h4>
      </div>
    </Card>
  );
};

export default Widget;
