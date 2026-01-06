'use client';

import SignInForm from '@/components/auth/sign-in-form';
import MainLayout from '@/components/layout/main-layout';

export default function LoginPage() {
  return (
    <MainLayout>
      <div className="flex justify-center items-center min-h-[60vh]">
        <SignInForm />
      </div>
    </MainLayout>
  );
}