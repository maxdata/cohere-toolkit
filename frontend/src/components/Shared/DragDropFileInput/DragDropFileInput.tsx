import { ReactNode, useState } from 'react';

import { Text } from '@/components/Shared/Text';
import { cn } from '@/utils';

export type FileAccept =
  | 'text/csv'
  | 'text/plain'
  | 'text/html'
  | 'text/markdown'
  | 'text/tab-separated-values'
  | 'application/msword'
  | 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  | 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  | 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
  | 'application/json'
  | 'application/ld+json'
  | 'application/pdf'
  | 'application/epub+zip';

export type DragDropFileInputProps = {
  id?: string;
  name?: string;
  label?: ReactNode;
  subLabel?: string;
  dragActiveLabel?: string;
  dragActiveDefault?: boolean;
  required?: boolean;
  accept?: FileAccept[];
  placeholder?: string;
  disabled?: boolean;
  readOnly?: boolean;
  className?: string;
  multiple?: boolean;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void | Promise<void>;
};

/**
 * File input that allows for drag and drop
 */
export const DragDropFileInput: React.FC<DragDropFileInputProps> = ({
  id,
  label = (
    <>
      Drag and drop files here or <u>browse files</u>
    </>
  ),
  subLabel = '.PDF or .TXT, Max 20MB',
  dragActiveLabel = 'Drop files to upload',
  dragActiveDefault = false,
  name,
  required,
  accept = ['application/pdf', 'text/plain'],
  placeholder = '',
  disabled = false,
  readOnly = false,
  multiple = false,
  className,
  onChange,
}) => {
  const [dragActive, setDragActive] = useState(dragActiveDefault);

  return (
    <div
      className={cn(
        'relative flex h-28 w-full flex-col items-center justify-center rounded-md border border-secondary-200 px-3 py-6',
        'transition duration-200',
        'border-dashed bg-secondary-50',
        {
          'border-solid bg-secondary-200': dragActive,
        },
        className
      )}
    >
      {dragActive ? (
        <Text className="max-w-[170px] text-center text-secondary-800">{dragActiveLabel}</Text>
      ) : (
        <>
          <Text className="max-w-[210px] text-center text-secondary-800">{label}</Text>
          <Text className="text-center text-secondary-700" styleAs="caption">
            {subLabel}
          </Text>
        </>
      )}
      <input
        id={id}
        className="absolute left-0 top-0 h-full w-full opacity-0"
        type="file"
        multiple={multiple}
        accept={accept.toString()}
        name={name}
        required={required}
        placeholder={placeholder}
        disabled={disabled}
        readOnly={readOnly}
        onChange={onChange}
        onDragEnter={() => setDragActive(true)}
        onDragOver={() => setDragActive(true)}
        onDragLeave={() => setDragActive(false)}
        onDrop={() => setDragActive(false)}
      />
    </div>
  );
};
