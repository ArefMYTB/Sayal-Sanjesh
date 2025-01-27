import { createContext, useState } from "react";
interface ThemeContextTypes {
  isDark: boolean;
  setIsDark: React.Dispatch<boolean>;
}
export const ThemeContext = createContext<ThemeContextTypes>(null);
const ThemeProvider = ({ children }: any) => {
  const [isDark, setIsDark] = useState<boolean>(false);

  const handleOnError = (error: Error, errorInfo: React.ErrorInfo) => {
    // Log the error to an error reporting service
    console.error("Error caught by error boundary:", error, errorInfo);
    // Update state to indicate an error has occurred
    setIsDark(true);
  };

  // if (isDark) {
  //   // You can customize the error message here
  //   return <div>Something went wrong. Please try again later.</div>;
  // }

  // Render children if no error occurred
  return (
    <ThemeContext.Provider value={{ isDark: isDark, setIsDark: setIsDark }}>
      {children}
    </ThemeContext.Provider>
  );
};

export default ThemeProvider;
