'use client';

import SignUpForm from '@/components/auth/sign-up-form';
import MainLayout from '@/components/layout/main-layout';

export default function SignUpPage() {
  return (
    <MainLayout>
      <div className="flex justify-center items-center min-h-[60vh]">
        <SignUpForm />
      </div>
    </MainLayout>
  );
}