import { Link, useRouteError } from "react-router";

interface RouterError {
  status?: number;
  statusText?: string;
  message?: string;
}

export default function ErrorPage() {
  const error = useRouteError() as RouterError;
  const status = error.status || 500;
  const message = error.statusText || error.message || "Something went wrong";

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="p-8 bg-white rounded-lg shadow-md text-center">
        <h1 className="text-5xl font-bold text-gray-800 mb-4">{status}</h1>
        <p className="text-lg text-gray-600 mb-6">{message}</p>
        <Link
          to="/"
          className="inline-block px-6 py-2 bg-indigo-600 text-white font-medium rounded hover:bg-indigo-700 transition"
        >
          Back to home
        </Link>
      </div>
    </div>
  );
}
