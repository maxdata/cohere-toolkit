import { RadioGroup } from '@headlessui/react';
import React from 'react';

import { DEFAULT_CHAT_TOOL } from '@/cohere-client';
import { OptionCard } from '@/components/Messages/Welcome/OptionCard';
import { Text } from '@/components/Shared';
import { useFocusComposer } from '@/hooks/actions';
import { useParamsStore } from '@/stores';
import { ConfigurableParams } from '@/stores/slices/paramsSlice';

export enum StartOptionKey {
  UNGROUNDED = 'ungrounded',
  WEB_SEARCH = 'web-search',
  DOCUMENTS = 'documents',
}

type StartOption = {
  title: string;
  description: string;
  features: string[];
  params: Partial<ConfigurableParams>;
  onChange?: VoidFunction;
};

/**
 * @description Renders the getting started options for new conversations
 */
export const StartOptions: React.FC<{
  selectedOption: StartOptionKey;
  onOptionSelect: (option: StartOptionKey) => void;
}> = ({ selectedOption, onOptionSelect }) => {
  const { setParams } = useParamsStore();
  const { focusComposer } = useFocusComposer();

  const START_OPTIONS: Record<StartOptionKey, StartOption> = {
    [StartOptionKey.UNGROUNDED]: {
      title: 'Chat',
      description: 'The model will respond without any sources and citations.',
      features: [
        'Job description generation: "Help me generate job description..."',        
      ],
      params: {
        tools: [],
        fileIds: [],
      },
    },
    [StartOptionKey.WEB_SEARCH]: {
      title: 'Candidate Discovery',
      description: 'Search and retrieve candidate profiles based on specified criteria from a comprehensive database.',
            features: [
                'Query candidate resumes: "Show me top resumes for a project manager..."',
                'Filter by skills and experience: "Find candidates with 5 years of experience in digital marketing..."'
            ],
      params: {
        tools: [{ name: DEFAULT_CHAT_TOOL }],
      },
    },
    [StartOptionKey.DOCUMENTS]: {
      title: 'Find Jobs',
      description: 'It will search jobs pool based on your query and return the top results.',
      features: ['Find jobs: "Give me top jobs as a software engineer..."'],
      params: {},
      onChange: () => {
        setTimeout(() => focusComposer(), 100);
      },
    },
  };

  const handleSelectOption = (key: StartOptionKey) => {
    const { params } = START_OPTIONS[key];
    onOptionSelect(key);
    setParams(params);
  };

  return (
    <div className="flex flex-col items-center gap-y-6">
      {/* <Text styleAs="h4">Choose an option to get started</Text> */}
      <RadioGroup
        value={selectedOption}
        onChange={(key: StartOptionKey) => {
          const { onChange } = START_OPTIONS[key];
          handleSelectOption(key);
          onChange?.();
        }}
        className="flex w-full flex-col justify-center gap-x-6 gap-y-4 pb-10 md:flex-row"
      >
        {(Object.keys(START_OPTIONS) as StartOptionKey[]).map((key) => {
          const option = START_OPTIONS[key];
          return <OptionCard key={key} value={key as StartOptionKey} {...option} />;
        })}
      </RadioGroup>
    </div>
  );
};
