import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { ChakraProvider } from "@chakra-ui/react";
import "./index.css";
import "react-toastify/dist/ReactToastify.css";
import {
  // useQuery,
  // useMutation,
  // useQueryClient,
  QueryClient,
  QueryClientProvider,
} from "@tanstack/react-query";

import App from "./App";
import { ToastContainer } from "react-toastify";
import ThemeProvider from "ThemeProvider";
// import ThemeProvider from "ThemeProvider";
const minsInMs = 1000 * 60 * 1;
const root = ReactDOM.createRoot(document.getElementById("root"));
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnMount: true,
      refetchOnReconnect: true,
      retry: true,
      staleTime: minsInMs,
    },
  },
});
root.render(
  <QueryClientProvider client={queryClient}>
    {/*  */}
    <ChakraProvider>
      <ThemeProvider>
        <BrowserRouter>
          <App />
          <ToastContainer />
        </BrowserRouter>
      </ThemeProvider>
    </ChakraProvider>
    {/*  */}
  </QueryClientProvider>
);
