export default function Footer() {
  return (
    <footer className="bg-gray-100 dark:bg-gray-800 py-6 border-t border-gray-200 dark:border-gray-700">
      <div className="container mx-auto px-4 text-center text-gray-600 dark:text-gray-400">
        <p>© {new Date().getFullYear()} Todo App. All rights reserved.</p>
      </div>
    </footer>
  );
}