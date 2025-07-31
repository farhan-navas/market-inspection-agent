import { createBrowserRouter } from "react-router";
import App from "./pages/App";
import DashboardPage from "./pages/Dashboard";
import ErrorPage from "./components/ErroBoundary";
import IndustryRegionCountryForm from "./components/IndustryRegionCountryForm";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/dashboard",
    element: <DashboardPage />,
  },
  {
    path: "/form",
    element: <IndustryRegionCountryForm />,
  
  }

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
