'use client';

import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/hooks/use-auth';
import { User } from '@/lib/types';
import { api } from '@/lib/api';

interface ProfileImageUploadProps {
  onImageChange?: (image: string) => void;
}

const ProfileImageUpload: React.FC<ProfileImageUploadProps> = ({ onImageChange }) => {
  const { user, isLoading, updateProfileImage } = useAuth();
  const [previewImage, setPreviewImage] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (user?.image) {
      setPreviewImage(user.image);
    } else if (user?.name || user?.email) {
      setPreviewImage(null);
    }
  }, [user]);

  const handleImageChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.type.match('image.*')) {
      setUploadError('Please select an image file (JPEG, PNG, GIF)');
      return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      setUploadError('File size exceeds 5MB limit');
      return;
    }

    setUploadError(null);
    setIsUploading(true);

    try {
      // Create preview
      const reader = new FileReader();
      reader.onload = async (e) => {
        const result = e.target?.result as string;
        setPreviewImage(result);

        // Update the user's profile image in the auth context
        if (updateProfileImage) {
          try {
            // In a real implementation, you would call the API to save the image to the backend
            // await api.updateProfileImage(user.id, result);

            await updateProfileImage(result);

            // Call the callback if provided
            if (onImageChange) {
              onImageChange(result);
            }
          } catch (error) {
            setUploadError('Error updating profile image. Please try again.');
            console.error('Error updating profile image:', error);
          }
        }

        setIsUploading(false);
      };
      reader.readAsDataURL(file);
    } catch (error) {
      setUploadError('Error processing image. Please try again.');
      setIsUploading(false);
      console.error('Error processing image:', error);
    }
  };

  const handleImageClick = () => {
    fileInputRef.current?.click();
  };

  const getInitials = () => {
    if (user?.name) {
      return user.name.charAt(0).toUpperCase();
    }
    if (user?.email) {
      return user.email.charAt(0).toUpperCase();
    }
    return '?';
  };

  if (isLoading) {
    return (
      <div className="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-700 animate-pulse flex items-center justify-center">
        <span className="text-gray-500">...</span>
      </div>
    );
  }

  return (
    <div className="relative">
      <div
        className={`w-10 h-10 rounded-full flex items-center justify-center cursor-pointer transition-all duration-200 ${
          previewImage
            ? 'ring-2 ring-blue-500 ring-offset-2 dark:ring-offset-gray-800'
            : 'bg-gray-200 dark:bg-gray-700'
        }`}
        onClick={handleImageClick}
      >
        {previewImage ? (
          <img
            src={previewImage}
            alt="Profile"
            className="w-full h-full rounded-full object-cover"
          />
        ) : (
          <span className="text-lg font-semibold text-gray-700 dark:text-gray-300">
            {getInitials()}
          </span>
        )}
      </div>

      {isUploading && (
        <div className="absolute inset-0 bg-black bg-opacity-50 rounded-full flex items-center justify-center">
          <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
        </div>
      )}

      {uploadError && (
        <div className="absolute -bottom-6 left-0 right-0 bg-red-500 text-white text-xs rounded px-2 py-1 whitespace-nowrap">
          {uploadError}
        </div>
      )}

      <input
        type="file"
        ref={fileInputRef}
        onChange={handleImageChange}
        accept="image/*"
        className="hidden"
      />
    </div>
  );
};

export default ProfileImageUpload;