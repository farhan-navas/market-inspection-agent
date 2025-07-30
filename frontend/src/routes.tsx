import { createBrowserRouter } from "react-router";
import App from "./pages/App";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },

  // temp page structure that i think we will use?
  //   {
  //     path: "/search",
  //     element: <SearchPage />,
  //   },
  //   {
  //     path: "/data",
  //     element: <DataPage />,

  //     // optional loader example for later when we want to fetch data before showing the page
  //     // loader: async () => { ... return data }
  //   },
]);
