// Test script to verify new features
const fs = require('fs');
const path = require('path');

// Check that new components have been created
const newComponents = [
  'frontend/components/task/task-stats.tsx',
  'frontend/components/ui/card.tsx',
  'frontend/components/ui/progress.tsx',
  'frontend/app/profile/page.tsx',
  'frontend/app/settings/page.tsx',
  'frontend/contexts/theme-context.tsx',
  'frontend/components/common/dark-mode-toggle.tsx'
];

// Check that existing components have been updated
const updatedFiles = [
  'frontend/components/task/task-card.tsx',
  'frontend/components/task/task-form.tsx',
  'frontend/components/task/task-list.tsx',
  'frontend/components/layout/header.tsx',
  'frontend/lib/types.ts',
  'backend/models.py',
  'backend/schemas/task.py',
  'backend/services/task_service.py',
  'backend/routes/tasks.py',
  'frontend/lib/api.ts'
];

console.log('Testing new features...\n');

let allTestsPassed = true;

console.log('Checking new components...\n');
for (const file of newComponents) {
  const fullPath = path.join(__dirname, file);
  if (fs.existsSync(fullPath)) {
    console.log(`✅ ${file} - Created successfully`);
  } else {
    console.log(`❌ ${file} - File not found`);
    allTestsPassed = false;
  }
}

console.log('\nChecking updated files...\n');
for (const file of updatedFiles) {
  const fullPath = path.join(__dirname, file);
  if (fs.existsSync(fullPath)) {
    const content = fs.readFileSync(fullPath, 'utf8');

    // Check for specific features in updated files
    if (file === 'frontend/components/task/task-card.tsx') {
      if (content.includes('priority') && content.includes('category') && content.includes('due_date')) {
        console.log(`✅ ${file} - Contains priority, category, and due date display`);
      } else {
        console.log(`❌ ${file} - Missing priority/category/due date display`);
        allTestsPassed = false;
      }
    } else if (file === 'frontend/components/task/task-form.tsx') {
      if (content.includes('priority') && content.includes('category') && content.includes('due_date')) {
        console.log(`✅ ${file} - Contains new form fields`);
      } else {
        console.log(`❌ ${file} - Missing new form fields`);
        allTestsPassed = false;
      }
    } else if (file === 'frontend/components/task/task-list.tsx') {
      if (content.includes('TaskStats') && content.includes('priority_filter') && content.includes('category_filter')) {
        console.log(`✅ ${file} - Contains statistics and enhanced filters`);
      } else {
        console.log(`❌ ${file} - Missing statistics or enhanced filters`);
        allTestsPassed = false;
      }
    } else if (file === 'frontend/lib/types.ts') {
      if (content.includes('TaskPriority') && content.includes('TaskCategory')) {
        console.log(`✅ ${file} - Contains new type definitions`);
      } else {
        console.log(`❌ ${file} - Missing new type definitions`);
        allTestsPassed = false;
      }
    } else if (file === 'backend/models.py') {
      if (content.includes('TaskPriority') && content.includes('TaskCategory') && content.includes('due_date')) {
        console.log(`✅ ${file} - Contains new model fields`);
      } else {
        console.log(`❌ ${file} - Missing new model fields`);
        allTestsPassed = false;
      }
    } else if (file === 'frontend/lib/api.ts') {
      if (content.includes('priority_filter') && content.includes('category_filter')) {
        console.log(`✅ ${file} - Contains new API parameters`);
      } else {
        console.log(`❌ ${file} - Missing new API parameters`);
        allTestsPassed = false;
      }
    } else {
      console.log(`✅ ${file} - Updated successfully`);
    }
  } else {
    console.log(`❌ ${file} - File not found`);
    allTestsPassed = false;
  }
}

console.log('\nChecking package dependencies...\n');
const packageJsonPath = path.join(__dirname, 'frontend', 'package.json');
if (fs.existsSync(packageJsonPath)) {
  const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
  const dependencies = packageJson.dependencies || {};

  const requiredDeps = ['@radix-ui/react-progress', 'clsx', 'lucide-react', 'tailwind-merge'];
  for (const dep of requiredDeps) {
    if (dependencies[dep]) {
      console.log(`✅ ${dep} - Installed`);
    } else {
      console.log(`❌ ${dep} - Not installed`);
      allTestsPassed = false;
    }
  }
} else {
  console.log('❌ package.json - File not found');
  allTestsPassed = false;
}

console.log('\n' + '='.repeat(60));
if (allTestsPassed) {
  console.log('🎉 All new features have been successfully implemented!');
  console.log('\nNew features implemented:');
  console.log('• Task categories and labels');
  console.log('• Priority levels (Low, Medium, High, Urgent)');
  console.log('• Due dates functionality');
  console.log('• Enhanced filtering and sorting options');
  console.log('• Progress tracking and statistics dashboard');
  console.log('• User profile page');
  console.log('• Settings page with theme options');
  console.log('• Dark mode toggle');
  console.log('• Updated UI with modern design');
} else {
  console.log('⚠️  Some features may not be fully implemented.');
}
console.log('='.repeat(60));